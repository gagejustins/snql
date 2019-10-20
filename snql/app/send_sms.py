from twilio.rest import Client

account_sid = 'AC9b504b347dadb70afebbbea3449caf5a'
auth_token = 'a9ce30f634d027e256ed9c8623b21160'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                    body = 'What are you wearing today? Enter a string to search, or an integer if you already know your sneaker_id.',
                    from_ = '+12074202312',
                    to = '+15162797371'
                )

print(message.sid)