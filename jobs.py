import random 

async def job_work(glumboAmount):
    jobs = [f"You became a ShackCord admin and earned<:glumbo:1003615679200645130>{glumboAmount}!", f"You worked at McDonald's as a janitor and earned<:glumbo:1003615679200645130>{glumboAmount}!", f"You sold your soul to ShackCord and earned <:glumbo:1003615679200645130>{glumboAmount}!", f"You sold lemonade on the road and earned<:glumbo:1003615679200645130>{glumboAmount}!", f"You started your own discord server and earned<:glumbo:1003615679200645130>{glumboAmount}!", f"You started a successful corporation and earned<:glumbo:1003615679200645130>{glumboAmount}!", f"You bought a book from the local library and found<:glumbo:1003615679200645130>{glumboAmount} in it!", f"You found <:glumbo:1003615679200645130>{glumboAmount} in an old jacket you thought you lost!", f"You became a ShackCord moderator and earned<:glumbo:1003615679200645130>{glumboAmount}!", f"You worked as a freelance writer and earned<:glumbo:1003615679200645130>{glumboAmount}!", f"You donated blood at a local hospital and earned<:glumbo:1003615679200645130>{glumboAmount}!", f"You tutored a student in math and earned<:glumbo:1003615679200645130>{glumboAmount}!", f"You delivered pizzas for a local pizzeria and earned<:glumbo:1003615679200645130>{glumboAmount}!", f"You participated in a survey and earned<:glumbo:1003615679200645130>{glumboAmount}!", f"You found a rare coin in your attic and sold it for<:glumbo:1003615679200645130>{glumboAmount}!", f"You won a lottery and earned<:glumbo:1003615679200645130>{glumboAmount}!", f"Your Youtube video went viral, you made <:glumbo:1003615679200645130>{glumboAmount}", f"Your boss laughed at Family Guy funny moment #78 you showed him, he paid you a bonus of <:glumbo:1003615679200645130>{glumboAmount}", f"You made earned<:glumbo:1003615679200645130>{glumboAmount} selling AI generated paintings as your own.", f"You typed $work and got <:glumbo:1003615679200645130>{glumboAmount}. Neat!", f"you entered an eating competition and won by eating the other participants. Your prize was <:glumbo:1003615679200645130>{glumboAmount}"]
    job = random.choice(jobs)
    return job

# status is either successful job(gives glumbo) or unsuccesful(removes glumbo)
async def job_crime(glumboAmount, status):
    success_jobs = [f"You succesfully robbed a bank and earned <:glumbo:1003615679200645130>{glumboAmount}!", f"You started a ShackCord revolution and earned <:glumbo:1003615679200645130>{glumboAmount}!", f"You stole money from ShackCord federal reserve and earned <:glumbo:1003615679200645130>{glumboAmount}!", f"You robbed UnbelievaBoat and got <:glumbo:1003615679200645130>{glumboAmount}!", f"You sold organs on the dark web and earned <:glumbo:1003615679200645130>{glumboAmount}!", f"You pirated Minecraft, it saved you <:glumbo:1003615679200645130>{glumboAmount}!", f"You recorded the Fnaf movie and sold it for <:glumbo:1003615679200645130>{glumboAmount}", f"You scammed <:glumbo:1003615679200645130>{glumboAmount} out of a lovely old lady. Don't you feel bad for that?"]
    unsuccess_jobs = [f"You tried robbing a grandma, but she was a professional wrestler. You ended up in a hospital and paid <:glumbo:1003615679200645130>{glumboAmount} for your recovery.", f"You robbed a bank, but slipped on the wet floor and police arrested you. You lost <:glumbo:1003615679200645130>{glumboAmount}", f"You didn't pay taxes from the money you stole, so the IRS fined you <:glumbo:1003615679200645130>{glumboAmount}", f"You were caught posting memes in #general, the moderators fined you <:glumbo:1003615679200645130>{glumboAmount}", f"You were caught recording the Fnaf movie in the cinema, they fined you <:glumbo:1003615679200645130>{glumboAmount}", f"you have robbed a local bank but forgot to take the loot home. Your equipment price was <:glumbo:1003615679200645130>{glumboAmount}", f"You shouted out the N word and got beaten up. Your medical bill was <:glumbo:1003615679200645130>{glumboAmount}", f"THE FOG. <:glumbo:1003615679200645130>{glumboAmount}"]

    if status == True:
        return random.choice(success_jobs)
    else:
        return random.choice(unsuccess_jobs)
    
async def job_slut(glumboAmount, status):
    success_jobs = [f"You sold your R34 art for <:glumbo:1003615679200645130>{glumboAmount}!", f"Your client liked it and paid you <:glumbo:1003615679200645130>{glumboAmount}", f"You started an OnlyFans and earned <:glumbo:1003615679200645130>{glumboAmount}", f"You sold your feet pics, this made you <:glumbo:1003615679200645130>{glumboAmount}!", f"You did the thug shaker in front of a live audience for <:glumbo:1003615679200645130>{glumboAmount}", f"You helped uncle jack off the horse and got <:glumbo:1003615679200645130>{glumboAmount}!"]
    unsuccess_jobs = [f"You got an STD and paid <:glumbo:1003615679200645130>{glumboAmount} to cure it", f"Your condom broke so you paid <:glumbo:1003615679200645130>{glumboAmount} for abortion", f"You fell asleep during the intercourse so you paid <:glumbo:1003615679200645130>{glumboAmount} as a compensation", f"You sold your R34 art but it sucked so much, police fined you <:glumbo:1003615679200645130>{glumboAmount} for drawing that", f"The authorities found your OnlyFans account and fined you <:glumbo:1003615679200645130>{glumboAmount} for tax evasion", f"You paid for a hot single mom in your area, it cost <:glumbo:1003615679200645130>{glumboAmount}!", f"You entered Poland expecting to see femboys, but instead you got beaten up by skinwalkers. Your medical bill was <:glumbo:1003615679200645130>{glumboAmount}"]
    if status == True:

        return random.choice(success_jobs)
    else:
        return random.choice(unsuccess_jobs)