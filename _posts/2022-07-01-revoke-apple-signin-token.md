---
title: A complete guide to revoke the Apple Sign in token
author: Diane Delallée
Date: 2022-08-010 12:32:00
categories: [Blog, Apple, ruby]
tags: [Apple, ruby]
---

## A bit of context

Since July 2022, Apple required that if you app provide a Apple Sign in  process you should also have a way to let the user delete his account.

If you only delete the user in your app, the client will still see the relation between your app and his apple account in his phone settings
(Settings -> Click on your name -> Password and Security -> Apps Using Apple ID)

The goal here is to have a proper procedure that will also revoke this token to prevent the user to have to do that manually.

## Step to do

1. Get the Apple Sign in token. This is a JWT. 
2. Create a private key in your apple developer account
3. Save your private key in your rails credentials
4. Generate your Apple client secret to be able to call the revoke API
5. Call the revoke API

## Frustration and tips
The [documentation](https://developer.apple.com/documentation/sign_in_with_apple/revoke_tokens) is not really explicit, neither the error returns !!!

### invalid client error

Good to know: when you try to get the Apple Jwt token, if you have the error `invalid client error`, the [documentation](https://developer.apple.com/documentation/sign_in_with_apple/errorresponse) will say: 
`The authorization grant or refresh token is invalid, typically due to a mismatched or invalid client identifier, invalid code (expired or previously used authorization code), or invalid refresh token.`

But that not all !

You can also have this error if you do not have put the right `content-type` in your request.
I spend a lot of time trying to understand why I get this error, when I finally understand that I was calling the Apple API with the `content-type: json`.

### Validity of access and refresh token of Apple

When the user sign in for the first time with his Apple Account, he will receive an access token. This token has a validity of 1 hour ! If you need to revoke the account of a user later you won't be able to use this token.

🤔 What I need to do?

You need to ask for the refresh token when the account his link for the first time, and save it in our DB. This is the only way I found to be able to revoke properly the Apple account.
This token does not have a time validity

So here is the step to be able to revoke unlink the Apple account later
1. Allow the user to sign in with the Apple login
2. if login work properly, call the Apple API to get the refresh token
3. Store this refresh token in DB
4. When the user want to revoke his account, find the token of the user and call the API to revoke it

that should be it

## Credentials in rails

You can find information in the [Rails's documentation ](https://edgeguides.rubyonrails.org/security.html#custom-credentials), but I will write a specific documentation about it soon

## Service to get all the Apple jwt, and being able to revoke a token.

here is our final service to be able to get and revoke the token properly.

```ruby
class AppleService
  APPLE_CLIENT_ID = "".freeze
  APPLE_KID = "ABCDE12345".freeze
  APPLE_ISSUER_ID = "QWERT98765".freeze

  class << self
    def generate_apple_jwt
      apple_private_key = OpenSSL::PKey.read(Credentials.apple_private_key)

      apple_jwt = JSON::JWT.new(
        iss: APPLE_ISSUER_ID,
        iat: Time.now.to_time.to_i,
        exp: 2.days.from_now.to_time.to_i,
        aud: "https://appleid.apple.com",
        sub: APPLE_CLIENT_ID
      )
      apple_jwt.kid = APPLE_KID

      apple_jwt.sign(apple_private_key, :ES256).to_s
    end
    
    def refresh_token(authorization_code:, user_id:)
      apple_jwt = generate_apple_jwt

      url = URI('https://appleid.apple.com/auth/token')
      http = Net::HTTP.new(url.host, url.port)
      http.use_ssl = true

      request = Net::HTTP::Post.new(url)
      request["content-type"] = 'application/x-www-form-urlencoded'
      request.set_form_data(
        {
          client_id: APPLE_CLIENT_ID,
          client_secret: apple_jwt,
          code: authorization_code,
          grant_type: 'authorization_code'
        }
      )
      response = http.request(request)
      if response.code == '200'
        refresh_token = JSON.parse(response.body)['refresh_token']
        AppleSignInToken.find_or_create_by(token: refresh_token, user_id:)
      elsif JSON.parse(response.body)['error_description'] == CODE_ALREADY_USER
        logger.error(
          "AppleSignInService refresh_token: authentication_code already use", user_id: user_id
        )
      else
        Honeybadger.notify(
          error_class: 'Exceptions::AppleApiNotAvailableError',
          error_message: response.inspect
        )
        raise Exceptions::AppleApiNotAvailableError
      end
    end

    def revoke_token(client_secret:, token:)
      url = URI("https://appleid.apple.com/auth/revoke")
      http = Net::HTTP.new(url.host, url.port)
      http.use_ssl = true

      request = Net::HTTP::Post.new(url)
      request["content-type"] = 'application/x-www-form-urlencoded'
      request.set_form_data(
        {
          client_id: APPLE_CLIENT_ID,
          client_secret:,
          token:,
          token_type_hint: 'access_token'
        }
      )

      response = http.request(request)
      if response.code == '200'
        puts "Well done the Apple SignIn token is revoked"
      else
        puts reponse.body
        raise StandardError, 'We can not achieve to revoke the token'
      end
    end
  end
end
```

and now to test it 

```shell
rails c 
apple_client_secret = AppleService.generate_apple_jwt

token = 'a JWT provided in your app. This is the JWT you want to revoke'

AppleService.revoke_token(client_secret: apple_client_secret, token:)
```


I hope it will help you !