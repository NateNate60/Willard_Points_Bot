import prawcore.exceptions as e
while True :
    try :
        # NateNate60's Willard Points Bot
        version = "3.1.1"

        print ("Starting Willard Points Bot version", version)

        # Module importation
        print ("Importing modules...", end='')
        import praw
        import config4 as config
        import time as t
        import datetime
        import os.path
        print ('done')
        print ("Loading features...", end='')

        # On or Off. You can still run it if off, but nothing will actually happen
        on = True

        # Set the tick
        tick = 0

        # Login function
        def login() :
            print ("Connecting to Reddit")
            print ("Authenticating...", end='')
            r = praw.Reddit(username = config.username,
                            password = config.password,
                            client_id = config.client_id,
                            client_secret = config.client_secret,
                            user_agent = "WillardPointsBot" + version)
            print ('done')
            return r


        """
        Core running functionality
        """


        # Retrieve the queue of transactions to be processed
        def retrieve() :
            with open ("transactions.txt", "r") as queuefile :
                queue = queuefile.read()
                queue = queue.split('\n')
            open('transactions.txt', 'w').close()

            return queue


        #Set the signature
        signature = "\n \n ^NateNate60's ^Willard ^Points ^Bot ^v" + version + ". ^Don't ^have ^an ^account? ^Use ^!newaccount. ^!info ^for ^information"
        #signature = "\n \n ^NateNate60's ^Willard ^Points ^Bot ^v" + version + "\n\n" + "Don't be alarmed if the bot replied to you more than once. This is because the bot keeps corrupting its own memory and I can't figure out why."

        # The acutal code
        def run_bot(r, tick, timen, queue, replied_to, time, blacklist) :
            if on == True :
                for trans in queue :
                    trans = str(trans)
                    if "~" in trans and "+" not in trans :
                        trans = trans.split('~')
                        user = trans[0]
                        if os.path.isfile (user + ".txt") :
                            with open (user + ".txt", 'r') as u :
                                balance = u.read()
                            balance = int(balance) - int(trans[1])
                            if balance < 0 :
                                balance = balance + int(trans[1])
                                notify (r, user, balance, trans[1], 0)
                            with open (user + ".txt", 'w') as s :
                                s.write(str(balance))
                            with open ('log.txt', 'a') as log :
                                log.write ("\n" + time + ' ' + user + " paid " + trans[1] + " WP.")
                                print (time + ' ' + user + " paid " + trans[1] + " WP.")
                            notify(r, user, balance, trans[1], '~')

                    elif "+" in trans and "~" not in trans :
                        trans = trans.split('+')
                        user = trans[0]
                        if os.path.isfile (user + ".txt") :
                            with open (user + ".txt", 'r') as u :
                                balance = u.read()
                            balance = int(balance) + int(trans[1])
                            with open (user + ".txt", 'w') as s :
                                s.write(str(balance))
                            with open ('log.txt', 'a') as log :
                                log.write ("\n" + time + ' ' + user + " gained " + trans[1] + " WP.")
                                print (time + ' ' + user + " gained " + trans[1] + " WP.")
                            notify(r, user, balance, trans[1], '+')
                if tick%2 == 0 :
                    for message in r.inbox.unread(limit = 5) :
                        if message.author.name != "Shut_Up_Exe_Bot" :
                            #For blacklisting
                            if "!black" in message.body.lower() or "unsub" in message.body.lower() or "ignore" in message.body.lower() :
                                message.reply ("Sorry to see you go. You have been temporarily blacklisted. Due to a technical problem, the bot cannot permanently blacklist you automatically." +
                                               " Pinging u/NateNate60 for permanent blacklisting. This ping WILL NOT WORK if this command was issued in a PM, so please contact NateNate60 yourself." + signature)
                                blacklist.append(message.author)
                                print (time, message.author, "requested to be blacklisted")
                            #For opening new accounts
                            if "!newacc" in message.body or "!openacc" in message.body or "!createacc" in message.body :
                                accname = str(message.author)
                                if not os.path.isfile(accname + ".txt") and "bot" not in message.body.lower() :
                                    accowner = accname
                                    with open (accname + ".txt", 'w') as newacc :
                                        newacc.write ("0")
                                    message.reply ('Account creation successful. '
                                                   + 'You will receive a one-time "signing" bonus of 10 Willard Points.' + signature)
                                    with open ('log.txt', 'a') as log :
                                        log.write ("\n" + time + ' ' + accowner + " opened an account.")
                                        print (time + ' ' + accowner + " opened an account.")
                                    with open ('transactions.txt', 'a') as transa :
                                       transa.write ('\n' + str(accname) + '+10')
                                else :
                                    if "bot" not in message.body.lower() :
                                        message.reply ('Something went wrong. Account creation failed. You probably already have an account. If you continue to receive this error, contact NateNate60. You can always try again.'
                                                       + signature)


                            #For querying information
                            elif "!inf" in message.body.lower() or "!help" in message.body.lower() :
                                message.reply ("NateNate60's Willard Points Bot version " + version + "\n \n" +
                                               "Willard Points Bot is a bot created by NateNate60 to conduct transactions in Willard Points. What are Willard Points, you say? WP is a completely useless" +
                                               ' joke currency that is issued to people saying "shut up exe" and making dank memes in r/townofsalemgame.' +
                                               " Commands may be issued to the bot using the NEUTRALEVIL protocol. \n \n" +
                                               "`!createaccount` will open a new account for you. I'll even give you 10 WP just for doing that. \n \n" +
                                               "`!bal [username]` to check [username]'s account balance. For example, `!bal Willard_Points_Bot` will query Willard_Points_Bot's account balance. \n \n" +
                                               "`!transfer [amount] [recepient]` will transfer [amount] Willard Points to [recepient]. \n \n" +
                                               "`[username]+[amount]` and `[username]~[amount]` will add and subtract [amount] WP from [username] respectively. \n \n" +
                                               "`!blacklist` to unsubscribe yourself from the Willard Points programme. Your account will be deleted in due time and the bot will no longer reply to your posts awarding WP. \n \n" +
                                               "As long as I see the command in my inbox I will process it. You can either reply to one of my messages, or compose a PM to me by clicking the little envelope button next" +
                                               ' to your name and then going to "compose new message". I cannot use the chat function of New Reddit yet. Stay tuned for more updates! If you have any questions, contact NatenNate60.')


                            #For moderators adding or removing money from people's accounts administratively.
                            elif "+" in message.body or '~' in message.body :
                                if message.author not in config.approved :
                                    message.reply ('You are not authorised to make that command.' + signature)
                                else :
                                    trans = message.body
                                    if "~" in trans :
                                        trans = trans.split('~')
                                        user = trans[0]
                                        if os.path.isfile(user + ".txt") :
                                            with open (user + ".txt", 'r') as u :
                                                balance = u.read()
                                            balance = int(balance) - int(trans[1])
                                            if balance < 0 :
                                                balance = 0
                                                message.reply ("That user does not have enough WP, so their balance was set to zero." + signature)
                                            else :
                                                message.reply ("The command completed successfully. \n \n"+ " ^Willard ^Points ^Bot ^v" + version)
                                            with open (user + ".txt", 'w') as s :
                                                s.write(str(balance))
                                            with open ('log.txt', 'a') as log :
                                                log.write ("\n" + time + ' ' + user + " was docked " + trans[1] + " WP by "  + str(message.author))
                                                print (time + ' ' + user + " was docked " + trans[1] + " WP by "  + str(message.author))
                                            notify(r, user, balance, trans[1], '~~')
                                        else :
                                            message.reply ("That account does not exist. Please contact NateNate60 for help." + signature)
                                    elif "+" in trans :
                                        trans = trans.split('+')
                                        user = trans[0]
                                        if os.path.isfile(user + ".txt") :
                                            with open (user + ".txt", 'r') as u :
                                                balance = u.read()
                                            balance = int(balance) + int(trans[1])
                                            message.reply ("The command completed successfully. " + signature)
                                            with open (user + ".txt", 'w') as s :
                                                s.write(str(balance))
                                            with open ('log.txt', 'a') as log :
                                                log.write ("\n" + time + ' ' + user + " was awarded " + trans[1] + " WP by "  + str(message.author))
                                            notify(r, user, balance, trans[1], '++')
                                        else :
                                            message.reply ("That account does not exist. Please contact NateNate60 for help." + signature)

                            #Balance checking
                            elif "!bal" in message.body :
                                payload = message.body.split(" ")
                                if len(payload) < 2 :
                                    message.reply ('Invalid syntax. Try !balance [username]')
                                else :
                                    if len(payload) == 1 :
                                        payload.append(message.author.name)
                                    if os.path.isfile(payload[1] + ".txt") :
                                        with open (payload[1] + ".txt", 'r') as acc :
                                            bal = acc.read()
                                        if payload[1] == message.author.name :
                                            message.reply("Your account currently has " + bal + " Willard Points." + signature)
                                        else :
                                            message.reply("That account currently has " + bal + " Willard Points." + signature)
                                    else :
                                        message.reply ("That account does not exist. Use !newaccount" + signature)
                            elif "!log" in message.body :
                                with open("log.txt",'r') as log :
                                    message.reply(log.read() + signature)
                            # Transferring
                            elif "!trans" in message.body :
                                print ('Detected transfer request.')
                                payload = message.body
                                payload = payload.split(' ')
                                if len(payload) == 2 :
                                    to = payload [2]
                                    try: 
                                        amt = int(payload [1])
                                        if amt < 0 :
                                            message.reply("Invalid amount. You cannot transfer a negative number of Willard Points.")
                                        else :
                                            fromfile = str(message.author) + ".txt"
                                            if os.path.isfile(fromfile) :
                                                if os.path.isfile(to + ".txt") :
                                                    with open (fromfile, 'r') as f :
                                                        balance = f.read()
                                                        balance = int(balance) - amt
                                                        if balance < 0 :
                                                            balance = balance + amt
                                                            message.reply("Invalid amount. You cannot transfer more points that you currently have. Your currently have " + str(balance) + ' WP.' + signature)
                                                        else :
                                                            print (time + ": " + message.author.name + "transferred " + str(amt) + " to " + to)
                                                            with open('log.txt', 'a') as log :
                                                                log.write('\n' + time + ": " + message.author.name + "transferred " + str(amt) + " to " + to)
                                                            with open ('transactions.txt', 'a') as trans :
                                                                trans.write("\n" + str(message.author) + "~" + str(amt))
                                                                trans.write('\n' + to + "+" + str(amt))
                                                else :
                                                    message.reply ("Invalid recepient. Make sure you spelled the recepient's username correctly and leave out the u/." + signature)
                                            else :
                                                message.reply ("Invalid sender. You do not have an account. Use !newaccount to create a new account." + signature)
                                    except ValueError :
                                        message.reply("Invalid amount. The amount must be a number." + signature)
                                else :
                                    message.reply("Invalid syntax. The syntax for transferring is `!transfer [amount] [recipient]`. If your comment has more than two spaces, this error will be raised.")
                            elif "shut up" in message.body.lower() :
                                message.reply ('no u (try `!blacklist`)' + signature)
                            elif "bad bot" in message.body.lower() :
                                message.reply ("shut up human (try `!blacklist`)" + signature)
                            elif "!isup" in message.body.lower() or "!stat" in message.body.lower() :
                                message.reply ("Online." + signature)
                            r.inbox.mark_read([message])




                #For awarding WP to good posts
                if timen%21600 < 60 :
                    print(time + ': Fetching submissions')
                    crp = get_crp()
                    for post in r.subreddit('townofsalemgame').hot(limit = 12) :
                        if post.stickied or not os.path.isfile(str(post.author) + ".txt") or post.score < 80 :
                            continue
                        elif post.score >= 80 and post.score < 150 :
                            tier = "FRAMER"
                        elif post.score >= 150 and post.score < 300 :
                            tier = "MAFIOSO"
                        elif post.score >= 300 and post.score < 500 :
                            tier = "BLACKMAILER"
                        elif post.score >= 500 and post.score < 1000 :
                            tier = "CONSIGLIERE"
                        elif post.score >= 1000 :
                            tier = "GODFATHER"
                        if post.id not in crp and post.score > 79:
                            award = 0
                            if tier == "FRAMER" :
                                award = post.score // 15
                            elif tier == "MAFIOSO" :
                                award = post.score // 20 + 3
                            elif tier == "BLACKMAILER" :
                                award = post.score // 20 + 5
                            elif tier == "CONSIGLIERE" :
                                award = post.score // 20 + 10
                            elif tier == "GODFATHER" :
                                award = 100
                            with open(str(post.author) + ".txt", 'r') as auth :
                                bal = int(auth.read())
                                bal = bal + award
                            with open(str(post.author) + ".txt", 'w') as auth :
                                auth.write(str(bal))
                            print(time + ": " + str(post.author) + " gained " + str(award) + " WP.")
                            with open('log.txt','a') as log :
                                log.write('\n' + time + " " + str(post.author) + " gained " + str(award) + " WP.")
                            post.reply ("Hello. Thank you for you wonderful post to our subreddit. I am the bot (that you subscribed to) that awards Willard Points to good posts. I am pleased"+
                                        " to inform you that your post has reached the " + tier + " tier. As such, I am awarding you " + str(award) + " Willard Points for this post. I will update" +
                                        " you if you earn more Willard Points. I check the top 12 posts ever six hours. Pinned posts are unfortunately not eligible. You've got " + str(bal) + " WP now.")
                            notify (r, post.author.name, bal, award, '+')
                        elif post.score > 79 and post.id in crp :
                            award = 0
                            if tier == "FRAMER" :
                                award = post.score // 15
                            elif tier == "MAFIOSO" :
                                award = post.score // 20 + 3
                            elif tier == "BLACKMAILER" :
                                award = post.score // 20 + 5
                            elif tier == "CONSIGLIERE" :
                                award = post.score // 20 + 10
                            elif tier == "GODFATHER" :
                                award = 100
                            if award != 0 :
                                with open(str(post.author) + ".txt", 'r') as auth :
                                    bal = int(auth.read())
                                    bal = bal + award
                                with open(str(post.author) + ".txt", 'w') as auth :
                                    auth.write(str(bal))
                                print(time + ": " + str(post.author) + " gained " + str(award) + " WP.")
                                with open('log.txt','a') as log :
                                    log.write('\n' + time + " " + str(post.author) + " gained " + str(award) + " WP.")
                                for cmt in post.comments :
                                    if cmt.author == r.user.me() and "that you subscribed to" in cmt.body :
                                        oldbody = cmt.body
                                        cmt.edit (oldbody + '\n\n' + "EDIT: It's me again! I found this post again on the front page, which means I can award more Willard Points to you! Here is " +
                                                  str(award) + " more Willard Points. It's now in the " + tier + " tier. Keep it up! You've got " + str(bal) + " WP now.")
                                notify (r, post.author.name, bal, award, '+')
                        crp.append(post.id)
                    print (time + ': Done fetching.')
                    write_crp(crp)
                write_comment_list(replied_to)

        def notify (r, user, balance, amt, sign) :
            if sign == '~' :
                r.redditor(user).message('Willard Points were debited from your account', str(amt) + " Willard Points were deducted from your account. \n \n"
                                         + 'You have ' + str(balance) + " Willard Points left.")
            elif sign == '+' and int(amt) > 1 :
                r.redditor(user).message('Willard Points were credited to your account', str(amt) + " Willard Points were added to your account. \n \n"
                                         + 'You have ' + str(balance) + " Willard Points now.")
            elif sign == '~~' :
                r.redditor(user).message('Willard Points were debited to your account', str(amt) + " Willard Points were deducted from your account. \n \n"
                                         + 'You have ' + str(balance) + " Willard Points left.")
            elif sign == '++' :
                r.redditor(user).message('Willard Points were credited to your account', str(amt) + " Willard Points were added to your account. \n \n"
                                         + 'You have ' + str(balance) + " Willard Points now.")
            elif sign == '0' :
                r.redditor(user).message('Attempted overdraw detected', "An attempt was made to overdraw your account. No points were deducted and the transaction has been cancelled. You have " + str(balance) + " WP.")

        def get_comment_list() :
            with open ("comments1.txt", "r") as f :
                comments_replied_to = f.read()
                comments_replied_to = comments_replied_to.split("\n")
            return comments_replied_to
        def write_comment_list(replied_to) :
            with open ('comments1.txt', 'w') as file :
                for i in replied_to :
                    file.write (i + '\n')
        def write_crp(crp) :
            with open ('crp.txt', 'w') as file :
                for i in crp :
                    file.write (i + '\n')
        def get_crp() :
            with open ("crp.txt", "r") as f :
                crp = f.read()
                crp = crp.split("\n")
            return crp
        print ('done')
        #NOTES
        # [OK] Test run_bot for a debiting statement in the queue file (which should be
        # in the form of 1234-5 where 1234 is debited 5 WP)
        #
        # [OK] Make sure to add a statement for crediting, too.
        #
        # [OK] Account creation should be quick and easy. The bot should periodically
        # check its inbox for messages with !createacc or !openacc or !newacc and make
        # a new account
        #
        # [OK] The bot should honour !credit [amt], !add, !debit, !sub commands only from
        # authorised users. Namely, NateNate60 and the mods of r/townofsalemgame
        #
        # [OK] The bot should be able to facilitate transactions between users with !transfer
        # between the account holder (VERIFY THIS TO STOP FRAUD) to any other account.
        # This may prove to be tricky to implement.
        #
        # [OK] The bot should honour !bal [acc #] commands from anyone, for any account.
        #
        # [OK] USERNAMES MUST NOT CONTAIN "+" OR "-"
        #
        # [OK] Mark read messages as read.
        #
        # [OK] Make the write_crt and read_crt functions to write the list crt to the file crt.txt.
        #
        # Make a file called crt.txt
        replied_to = get_comment_list()
        r = login()
        blacklist = config.blacklist
        time = datetime.datetime.fromtimestamp(t.time()).strftime('%Y-%m-%d %H:%M:%S')
        print ("Right now, it's " + time)
        while True :
            replied_to = get_comment_list()
            tick += 1
            timen = int(t.time())
            time = datetime.datetime.fromtimestamp(t.time()).strftime('%Y-%m-%d %H:%M:%S')
            queue = retrieve()
            run_bot(r, tick, timen, queue, replied_to, time, blacklist)
            if tick == 1 :
                print (time + ": The bot has successfully completed one cycle.")
            elif tick == 5 :
                print (time + ": The bot has successfully completed five cycles.")
            elif tick%10 == 0 and tick < 99 :
                print (time + ": The bot has successfully completed " + str(tick) + " cycles.")
            elif tick%100 == 0 and tick < 999 :
                print (time + ": The bot has successfully completed " + str(tick) + " cycles.")
            elif tick%1000 == 0 and tick > 999:
                print (time + ": The bot has successfully completed " + str(tick) + " cycles.")

            t.sleep(10)
    except e.RequestException :
        print ('The bot crashed with RequestException. Restarting...')
        continue
    except e.ResponseException :
        print ('The bot crashed with Error 503: ResponseException. Restarting...')
        continue
    except PermissionError :
        print ('The bot crashed with PermissionError. Restarting...')
        continue
    except e.Forbidden :
        print ('The bot crashed because it recieved a 503 HTTP error. Restarting...')
        continue












