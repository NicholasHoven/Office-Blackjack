# Office Blackjack!

Welcome to Office Blackjack!, the definitive blackjack experience on GitHub! I built Office BlackJack simply as a challenge to myself. I had used Python Tkinter frequency in my work to make simplistic applications for my team. After doing that for a few months I decided that I and wanted to try to push the library to its absolute limits. Thus the idea for a full stack video game was born!

![game_demo](https://github.com/user-attachments/assets/e197b0e4-36f5-43ea-8e1f-e6ebdbb1c5a4)

1.  **Place Your Bet:** Before each hand, you'll place a wager from your starting balance.
2.  **The Deal:** You and the dealer will each receive two cards. One of the dealer's cards will be face down.
3.  **Player's Turn:** Look at your hand and decide whether to "Hit" (take another card) or "Stand" (keep your current hand).
    * You can hit multiple times, but if your hand's total exceeds 21, you "Bust" and lose your bet.
    * If you reach a total of 21 with your first two cards, you have "Blackjack!" (this usually pays out at 1.5 times your bet, provided the dealer doesn't also have Blackjack).
4.  **Dealer's Turn:** Once you stand or bust, the dealer reveals their face-down card.
    * The dealer must hit if their hand's total is less than 17.
    * The dealer must stand if their hand's total is 17 or more.
5.  **Determine the Winner:**
    * If your hand's total is higher than the dealer's (without busting), you win your bet.
    * If the dealer busts and you haven't, you win.
    * If you bust, you lose your bet.
    * If your hand's total is the same as the dealer's, it's a "Push," and you get your bet back.
    * If the dealer has Blackjack and you don't, you lose.

## Game Interface

The game features a simple and intuitive interface:

* **Your Hand:** Your cards will be displayed at the bottom of the screen.
* **Dealer's Hand:** The dealer's cards will be shown at the top. One card will initially be face down.
* **Score:** The current total of your hand and the dealer's visible hand will be displayed.
* **Betting Area:** Use the virtual chips to place your bet before each round.
* **Action Buttons:** "Hit" to take another card, "Stand" to end your turn, and "Play" to start a new round after placing your bet.
* **Balance:** Your current in-game currency will be displayed.
