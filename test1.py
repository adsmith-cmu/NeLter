    def reset_round(self):
        self.next_player(self.button)
        self.closing_action = self.button
        self.current_bet = [0 for _ in self.players]
        self.relative_min_raise = self.absolute_min_raise


    def bet(self, amount):
        player = self.players[self.action]
        call_price = max(self.current_bet) - self.current_bet[self.action]
        min_raise = call_price + self.relative_min_raise
        if player.stack > call_price:
            amount = max(amount, min(min_raise, player.stack))
            player.stack -= amount
            self.pot += amount
            self.relative_min_raise = amount - call_price
            self.closing_action = self.action
            self.next_player()
        else:
            self.call()
        

    def call(self):
        player = self.players[self.action]
        call_price = max(self.current_bet) - self.current_bet[self.action]
        if player.stack > 0 or call_price <= 0:
            player.stack -= min(call_price, player.stack)
            self.pot += min(call_price, player.stack)
            self.current_bet[self.action] += min(call_price, player.stack)

            self.next_player() 
            if self.closing_action == self.action:
                self.progress_game() 
        else:
            self.fold()

        
    def fold(self):
        call_price = max(self.current_bet) - self.current_bet[self.action]
        if call_price > 0:
            self.players.pop(self.action)
            self.current_bet.pop(self.action)

        if len(self.players == 1):
            self.showdown()
        else:
            self.next_player() 
            if self.closing_action == self.action:
                self.progress_game() 










    def take_turn(self, amount):
        player = self.players[self.action]
        amount = min(amount, player.stack)
        # Player Raises
        if amount >= self.current_wager + self.relative_min_raise:
            player.stack -= amout
            self.pot += amout
            self.relative_min_raise = amout - self.current_wager
            self.closing_action = self.action
            self.next_player()
            print(f'Player: {self.action} raises')
        else:
            # Player Folds
            if wager < self.current_wager:
                self.players.pop(self.action)
                print(f'Player: {self.action} folds')
            # Player Calls or Checks
            else:
                player.stack -= wager
                self.pot += wager
                print(f'Player: {self.action} calls')

            if self.closing_action == self.action:
                self.progress_game() 
            else:
                self.next_player() 