# Matrix Invite Bot

Our primary Matrix Space is Private with Federation. The goal was to allow people to reuse existing matrix accounts.
We create new matrix users on the home server for people who don't have an existing matrix account and probably won't use one outside of this.

tuwunel doesn't allow us to auto join or auto invite users to a private room / space, so this bot will invite users to join the primary space whenever a new member joins a public unfederated holding room (set using `auto_join_rooms`).
