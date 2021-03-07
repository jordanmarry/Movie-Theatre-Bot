
import discord
import imdb 
import asyncio

from discord.ext import tasks, commands 

f = open('token.txt', 'r')
token = f.read()

client = commands.Bot(command_prefix = '!')

class Movie:
    def __init__(movieList, name=None, date=None, time=None):
        movieList.name = name
        movieList.date = date
        movieList.time = time
        movieList.next = None

class MovieList:
    def __init__(movieList):
        movieList.headval = None
        movieList.num = 0

listOfMovies = MovieList()



#
#
#   This method tells that the bot is ready to go. 
#
#



#Changes Presence of Bot to Playing !commands for help
#Prints Bot Started to know that the Bot is working
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="!commands for help"))
    print('Bot Started!')



#
#
#   This method prints out the commands lists in an embedded message.
#
#



#Makes an embedded message putting an author, fields of commands, and footer. Then prints out the message.
@client.command()
async def commands(ctx):
    embed = discord.Embed(title="Movie Bot Commands", color=0xFF7F50)
    embed.set_author(name="Movie Bot", icon_url="https://images.unsplash.com/photo-1485846234645-a62644f84728?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1340&q=80")
    embed.add_field(name="*!add (Movie Title)*", value="Sets a date and time for the movie.", inline=False)
    embed.add_field(name="*!clear*", value="Clears the Movie Night List.", inline=False)
    embed.add_field(name="*!edit (Number)*", value="Edit a specific movie the Movie Night List. The numbers are located from !list.", inline=False)
    embed.add_field(name="*!list*", value="Gives a list of all the movie nights.", inline=False)
    embed.add_field(name="*!search (Movie Title)*", value="Searches for a movie.", inline=False)
    embed.add_field(name="*!remove (Number)*", value="Removes a movie night. The numbers are located from !list.", inline=False)
    embed.set_footer(text= "Made by: @RabbiT")
    await ctx.channel.send(embed=embed)
    return
    


#
#
#   This method searches throughout IMDb and returns the title, directors, and the plot of the movie.
#
#



#This is the !search command communicates between bot and user to find the movie they are searching for. 
@client.command()
async def search(ctx, *args):
    author = ctx.message.author.mention
    #This checks if the message is the sent from the original user.
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    # Takes args and makes it into a string
    msg = ""
    for s in args:
        msg += s + " "
    

    #The Bot says is this the correct movie
    #The bot waits for the user to respond yes or no
    await ctx.channel.send('Is this the correct movie ' + author + "? **" + msg + "** | Yes or No")
    msg2 = await client.wait_for('message', check=check, timeout= 20)

    #This if statement checks if the user says yes and continues with the program
    if msg2.content.lower() == 'y' or msg2.content.lower() == 'yes':
        ia = imdb.IMDb() 
        # movie name 
        name = msg
  
        # searching the movie 
        search = ia.search_movie(name) 

        # grabs the id of the movie
        try:
            id= search[0].movieID
            # gets the movie and all of the information about it
            movie = ia.get_movie(id)
            title = movie.get('title')
            embed = discord.Embed(title=title, color=0xFF7F50)
            embed.set_footer(text= "Made by: @RabbiT")
            embed.set_author(name="Movie Bot", icon_url="https://images.unsplash.com/photo-1485846234645-a62644f84728?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1340&q=80")
        
            s= ''

            # adds a rating to the embed
            rating = movie.data['rating']
            st= str(rating) + " out of 10" + '\n'
            embed.add_field(name="Rating: ", value=st, inline=False)

            # adds directors to the list 
            for director in movie['directors']:
                s += (director['name'] + "\n")

            # adds the directors to the embed
            s + '\n'
            embed.add_field(name="Directors: ", value=s, inline=False)

            # adds plot to the embed. Gets rid of the author at the end.
            plot = movie['plot'][0]
            plot_wo = plot.split(":", 1)
            plot2 = plot_wo[0] 
            plot2 + '\n'
            embed.add_field(name="Plot: ", value=plot2, inline=False)

            await ctx.channel.send(embed=embed)

        except:
            await ctx.channel.send("Movie Not Found. Make Another Search Please! " + author)                                      # Change this to repeat
            return
        
        
    #This else if checks if the user says no and tells them to search again
    elif msg2.content.lower() == 'n' or msg2.content.lower() == 'no':
        await ctx.channel.send("Make Another Search Please! " + author)                                                           # Change this to repeat
        return

    #This else says that you've entered an Unknown Input
    else:
        await ctx.channel.send("Unknown Input. Make Another Search Please! " + author)                                            # Change this to repeat
        return


  
#
#
#   This method sets a date for the movie night.
#
#



@client.command()
async def add(ctx, *args):
    author = ctx.message.author.mention

    #This checks if the message is the sent from the original user.
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
                                                                                                                                    # Check if Word comes after
    
    # Takes args and makes it into a string
    msg = ""
    for s in args:
        msg += s + " "
                                                                                    
    
    ia = imdb.IMDb()
    # movie name
    name = msg
  
    # searching the movie 
    search = ia.search_movie(name) 

    # if movie is found goes through try if not except (DOES NOT DO THIS | FIX)
    try:
        
        id= search[0].movieID

        await ctx.channel.send('Enter a Date (--/--/----) ' + author)                                                               # Add check if right format

        date = await client.wait_for('message', check=check, timeout= 20)

        await ctx.channel.send('Enter a Time (--:-- PM/AM) ' + author)                                                              # Add check if right format

        time = await client.wait_for('message', check=check, timeout= 20)

        # Confirms with the user if the adding is correct 
        s = "**Is This Right?** " + author + "\n**Movie:** " + msg + "\n**Date:** " + date.content + "\n**Time:** " + time.content + "\nYes or No?"

        await ctx.channel.send(s)

        msg2 = await client.wait_for('message', check=check, timeout= 20)

        # If user says Y then adds if N then says try again
        if msg2.content.lower() == 'y' or msg2.content.lower() == 'yes':

            if listOfMovies.num == 0:
                listOfMovies.headval = Movie(msg, date.content, time.content)
                listOfMovies.headval.next = None
                listOfMovies.num += 1

            else:
                curr = listOfMovies.headval
                while curr.next is not None:
                    curr= curr.next

                new = Movie(msg, date.content, time.content)

                curr.next = new

                listOfMovies.num += 1

            await ctx.channel.send("Added Successfully! " + author)
            return

        else:
            await ctx.channel.send("Try Again!")                                                                                        # Make Repeat
            return

    except:
        await ctx.channel.send("Movie Not Found. Try Again " + author)
        return



#
#
#   This method prints out the list of the movie nights occurring
#
#



@client.command()      
async def list(ctx):
    author = ctx.message.author.mention
    embed = discord.Embed(title="Movie Night List", color=0xFF7F50)
    embed.set_footer(text= "Made by: @RabbiT")
    embed.set_author(name="Movie Bot", icon_url="https://images.unsplash.com/photo-1485846234645-a62644f84728?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1340&q=80")
    
    if listOfMovies.num == 0:
        await ctx.channel.send("No Movie Nights! " + author)
        return

    else:
        printMovie = listOfMovies.headval

        num = 1
        while printMovie is not None:
            s = "**Date:** " + printMovie.date + '\n**Time:** ' + printMovie.time + '\n\n'
            embed.add_field(name=str(num) + ". " + printMovie.name, value=s, inline=False)
            printMovie = printMovie.next
            num += 1

        await ctx.channel.send(embed=embed)
        return





#
#
#   This method removes a date for the movie night 
#
#



@client.command()
async def remove(ctx, num):
    
    author = ctx.message.author.mention

    number = listOfMovies.num

    curr = listOfMovies.headval
    
    numInt = int(num)

    if number == 0:
        await ctx.channel.send("No Movie Nights! " + author)
        return


    if numInt == 1:
        # if number == 1 remove the node and set the list to nothing
        if number == 1:
            listOfMovies.headval = None

        # else make next node head
        else:
            listOfMovies.headval = curr.next

        listOfMovies.num -=1
        await ctx.channel.send("Successfully Removed " + author)
        return 

    elif numInt == number:
        i = 1

        # traverse up till num-1 is reached
        while i < (numInt-1):
            curr = curr.next
            i += 1

        # set next to none
        curr.next = None

        listOfMovies.num -=1

        await ctx.channel.send("Successfully Removed " + author)
        return

    elif numInt > 1 and numInt < number:
        
        # make a prev 
        prev = None
        i = 1

        # traverse till num is reached
        while i < numInt:
            prev = curr 
            curr = curr.next
            i += 1

        # make prev next equal to curr.next
        prev.next = curr.next

        listOfMovies.num -=1

        await ctx.channel.send("Successfully Removed " + author)
        return 

    else:
        await ctx.channel.send("Invalid Number! Try Again! " + author)
        return 



#
#
#   This method clears the whole entire Movie List
#
#



@client.command()
async def clear(ctx):
    author = ctx.message.author.mention

    # Makes the head list equal None and resets the number of movies in the list
    listOfMovies.headval = None
    listOfMovies.num = 0

    await ctx.channel.send("Movie Night List Cleared")
    return



#
#
#   This method edits a certain Movie Night
#
#



@client.command()
async def edit(ctx, num):
    author = ctx.message.author.mention

    number = listOfMovies.num

    curr = listOfMovies.headval
    
    numInt = int(num)

    ia = imdb.IMDb()

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    # Checks if the list is empty
    if number == 0:
        await ctx.channel.send("List is Empty! " + author)
        return 

    # Checks if the number given is larger that the number of Nodes
    if numInt > number:
        await ctx.channel.send("Invalid Number! " + author)
        return

    i = 1

    # accesses the node in the linked list
    while i is not numInt:
        curr = curr.next
        i+= 1

    # Waits for a movie name to be put into chat 
    await ctx.channel.send('Enter a Movie ' + author)

    movie = await client.wait_for('message', check=check, timeout= 20)

    name = movie.content

    # searching the movie 
    search = ia.search_movie(name)

    try:

        # gets movie id. if cannot get the id because the movie doesnt exist 
        id= search[0].movieID

        # waits for a date to be put into chat
        await ctx.channel.send('Enter a Date (--/--/----) ' + author)                                                               # Add check if right format

        date = await client.wait_for('message', check=check, timeout= 20)

        # waits for a time to be put into chat
        await ctx.channel.send('Enter a Time (--:-- PM/AM) ' + author)                                                              # Add check if right format

        time = await client.wait_for('message', check=check, timeout= 20)

        print(movie.content)
        print(date.content)
        print(time.content)

        # changes the value of everything in the node
    
        curr.name = movie.content
        curr.date = date.content
        curr.time = time.content

        await ctx.channel.send("Editted Successfully! " + author)

        return

    except:
        # if movie not found then this is put into the chat
        await ctx.channel.send("Invalid Movie! Try Again! " + author)
        return




client.run(token)

