# Race Condition Vulnerability Walkthrough
#### By Siddhant Das (Sid Das on Canvas) - 100830959
## Description
Buy the PS5 in <b> the Shop™</b>.
## Prerequisites
### Knowledge requirements
- HTTP requests
- Python
- Multithreading

### Tool requirements
- BurpSuite
- Python
- IDE of choice

## Level 1: No Security
After running the application, we will first log into Very Buggy App (VBA) to access our challenge (If you don't have an account, go to registration).

![](./screenshots/1.png)

Then we select the challenge called "Race Condition Vulnerability". 

![](./screenshots/2.png)

Now that we are logged in and we can see the shop's interface, we want to buy the PS5. But our dilemma is that we only have $200 in our account and the PS5 is $500. We can buy any item and sell it back for the same price.

![](./screenshots/3.png)

![](./screenshots/4.png)

When we hit sell, it triggers the `/sell` endpoint with an `id` of the inventory item. So we will exploit this endpoint to sell the lego set multiple times before it leaves the inventory. So we fire up BurpSuite and intercept the sell POST request.

![](./screenshots/5.png)

Then we send the request to the Burp Intruder and hit Ctrl+R repeatedly to send duplicates to the repeater (20 should suffice)

![](./screenshots/6.png)

After that click on the 3 dotted button and "create tab group". Select all the tabs and put them in the tab group:

![](./screenshots/7.png)

Select the arrow in the request and select "send group in parallel" and then hit send.

![](./screenshots/8.png)

Now go refresh the application and now we can see that we have an extra $300.

![](./screenshots/9.png)

With this extra money, we can finally afford that PS5, so go ahead and buy it.

![](./screenshots/level1_final.png)

Congratulations on completing the race condition bug bounty.

## Level 2: Some Security
We can go ahead and solve this on next level which is medium security level or rather "Some Security". Start by setting your difficulty to "Some Security" in the difficulty tab.

![](./screenshots/2_1.png)

Whenever, we buy something, we can't sell it back anymore or can't see the sell id. 

![](./screenshots/2_2.png)

So we will intercept a buy request.

![](./screenshots/2_3.png)

Rename the buy endpoint to sell (While `/sell` is gone from client side, it is still exposed as an API).

![](./screenshots/2_4.png)

Since we are selling the Lego Set and the `product_id` is 3. We will put a request parameter called `product_id=3` and

![](./screenshots/2_5.png)

Just like level 1, we follow the steps and duplicate them into a tab group.

![](./screenshots/2_6.png)

Now we will set them to be sent in parallel and hit send.

![](./screenshots/2_7.png)

Now finally we have enough money to buy the PS5 and complete challenge on level 2.

![](./screenshots/2_8.png)

We have fully exploited a limited run race condition vulnerability. 

![](./screenshots/level2_final.png)

## Level 3: Maximum Security

Now change the difficulty to maximum security.

![](./screenshots/3_1.png)

This the final level and I have made impossible to solve this challenge because the vulnerable endpoint `/sell` is patched to not work anymore for race condition bug.

![](./screenshots/3_2.png)

Even if you try, you will get this message "Lock can't be processed".

![](./screenshots/3_3.png)

How I have secured the application from vulnerability is explained in the Behind the Scenes section.

## Behind the Scenes

The app runs on flask backend and it using server side rendering to serve html "templates" as well as static files (CSS and JS).