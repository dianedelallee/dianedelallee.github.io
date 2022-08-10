---
title: Fight with changelog conflicts
author: Diane Delallée 
date: 2021-09-23 11:12:00 +0100 
categories: [Blog, ruby]
tags: [ruby, Changelog]
---

If you use a changelog to document changes in your code in a code base where several developers works, you probably have to fix changelog file conflicts.

At [QoQa](https://www.qoqa.ch/fr), we have this problem a lot and it was really time consuming for everyone to resolve this kind of stupid conflicts.

## Previous way of handling changelog

1. Create a branch
2. Make your changes
3. Update the file `CHANGELOG.md`, create the proper section (## fixed, ## added, ...) add a line to explain quickly your changed
4. Create a Pull Request 
5. Fix conflict to be able to merge your branch in the "staging" one because others developers have also touch `CHANGELOG.md`

## New way of handling changelog - ByeBye conflicts

1. Create a branch
2. Make your changes
3. Create a file under the repo changelog/<name_of_the_section_wanted> <br>
   ex:  `changelog/fixed/my_new_file.md`<br>
   `changelog/added/my_new_feature.md`
4. Add a line to explain quickly your changed
5. Create a Pull Request
6. Merge your branch into the "staging" one !!!

Okay but with this technics no one is touching the `CHANGELOG.md` file and there a lot of new files. So How does this works?

### What we have done and how it works

1. We have created several folders under the `changelog` folder that represents the differents section that will appears in the `CHANGELOG.md` file
2. We have create a file `changelog/release_name.md` that will contains only the name of the release to display in the `CHANGELOG.md` file
3. We have created a rake task that will loop on all files presents in each folders, concatenates those information, add it to the `CHANGELOG.md` file and finally removed the file under the `changelog` folder <br>
   I will explain it later
4. Create a Github Action to execute this task only when we merge the "staging" branch into the "master" one.

### rake task explanation
```ruby
# Class to handle changelog
class ChangelogManagerService
  EXCLUDE_VARS = %w[. ..].freeze
  RELEASE_TITLE  = './changelog/release_name.md'.freeze

  def initialize
    @changelog_to_add = ''

    if File.exist?(RELEASE_TITLE)
      @release_name = File.read(RELEASE_TITLE)
    else
      now = Time.zone.now.strftime("%Y.%m.%d-%H:%M")
      @release_name = "## [stowaway-changes.#{now}]\n"
    end
  end

  def create_new_content
    # Function to create the text that will be added to the changelog
    create_unreleased_changelog
    add_changelog_subtitle
    file = File.read('./CHANGELOG.md')
    "#{@changelog_to_add}#{file}"
  end

  def write_new_changelog
    # Function that will get the content, write it in the changelog file and will delete individual changelog files
    new_content = create_new_content
    File.open('./CHANGELOG.md', 'w') { |line| line.puts new_content }
    clear_unreleased_files
  end

  private

  def add_changelog_subtitle
    # Function that will concatenate the release name and the content of all individual changelog
    return if @changelog_to_add.empty?

    @changelog_to_add = "#{@wagon_name}#{@changelog_to_add}\n"
  end

  def clear_unreleased_files
     # Function that will loop on each folders inside `changelog` folder and call the delete function and will delete the file `changelog/release_name.md`
    folders = Dir.entries('./changelog/').reject { |entry| (EXCLUDE_VARS.include? entry) }
    folders.each do |folder|
      delete_files(path: "./changelog/#{folder}")
    end
    File.delete(WAGON_TITLE) if File.exist?(RELEASE_TITLE)
  end

  def concatenate_files(list_of_files:)
    # Loop on a list of files and will concatenate the content to create the text that will appear in the final changelog
    list_of_files.each do |file|
      File.readlines(file).each do |line|
        @changelog_to_add << line.to_s
      end
      @changelog_to_add << "\n" unless File.read(file)[/\n$/]
    end
  end

  def subpart_unreleased_changelog(path:, title:)
    # Get the list of files in a folder and call the concatenate_files function only if there is file in this folder
    files = Dir.glob("#{path}/**/*").select { |e| File.file? e }.reject { |i| i == "#{path}/README.md" }
    if files.length.positive?
      @changelog_to_add << "\n#{title}\n\n"
      concatenate_files(list_of_files: files)
    end
  end

  def create_unreleased_changelog
    # Loop on all folders og changelog and call subpart_unreleased_changelog to do the job
    folders = Dir.entries('./changelog/').reject { |entry| (EXCLUDE_VARS.include? entry) }
    folders.each do |folder|
      subpart_unreleased_changelog(path: "./changelog/#{folder}", title: "### #{folder.capitalize}")
    end
  end

  def delete_files(path:)
    # Function that will delete all the files present in a folder except the one called READMDE.md 
    files = Dir.glob("#{path}/**/*").select { |e| File.file? e }.reject { |i| i == "#{path}/README.md" }
    files.each do |file|
      File.delete(file)
    end
  end
end
```

And that's it, now we do not have to solve some conflicts with our changelog.

If anything is not clear enough or if you would like to discuss it, feel free to contact me.