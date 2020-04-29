---
title: Guard file
author: Diane Delallée
date: 2019-01-21 20:55:00 +0800
categories: [Blog, Configuration]
tags: [guard]
---

Guardfile to run :

    pylint
    pep8 through flake8
    mypy
    tests

associated to the file you just saved.

```bash
guard :shell do
  watch(/(?.*\.py)/) do |m|
    file = m[:path]
    exclusion = %w(__pycache__ /migrations/ _BASE_ _REMOTE_ _BACKUP_ _LOCAL_)
    if exclusion.none? { |e| file.include? e }
      command_pylint = "pylint --rcfile=../.pylintrc --load-plugins=pylint_django #{file}"
      puts '', '', "###  Running: #{command_pylint}"
      if not system(command_pylint)
        n "Pylint issues in #{file}", "Pylint", :failed
      end

      command_pep8 = "flake8 #{file}"
      puts '', '', "###  Running: #{command_pep8}"
      if not system(command_pep8)
        n "pep8 issues in #{file}", "pep8", :failed
      end

      command_mypy = "mypy --follow-import=silent #{file}"
      puts '', '', "###  Running: #{command_mypy}"
      if not system(command_mypy)
        n "mypy issues in #{file}", "mypy", :failed
      end
    end
  end
  watch(/(?.*?\/)(?.*\/)?(?.*)\.py/) do |m|
    testModule = ""
    testFile = "#{m[:app]}tests/#{m[:path]}test_#{m[:filename]}"
    if File.file? "#{testFile}.py"
      testModule = testFile.gsub "/", "."
    end
    testFolder = "#{m[:app]}tests/#{m[:path]}#{m[:filename]}"
    if File.directory? testFolder
      testModule = testFolder.gsub "/", "."
    end
    if not testModule.empty?
      command = "python manage.py test --keepdb #{testModule}"
      puts '', '', "###  Running: #{command}"
      if not system(command)
        n "Test errors for #{testModule}", "Django Tests", :failed
      end
    end
  end
  watch(/(?.*\/tests\/(.*\/)?test_.*)\.py/) do |m|
    testModule = m[:filepath].gsub "/", "."
    command = "python manage.py test --keepdb #{testModule}"
    puts '', '', "###  Running: #{command}"
    if not system(command)
      n "Test errors for #{testModule}", "Django Tests", :failed
    end
  end
end

notification  :tmux,
  display_message: true,
  timeout: 2

notification :terminal_notifier if `uname` =~ /Darwin/
```

On your terminal you have to run

`bundle exec guard`
