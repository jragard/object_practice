class PokerHand(object):

    def __init__(self, hand):
        self.hand = hand

    def switch_letters(self, hand):
      
        # Switches out letter cards (A, K, Q, J, or T) to numbers representing
        # their values, which makes it easier to rank hands later
        hand_no_letters = []
        hand_tuples = []
        hand_dict = {}
      
        letter_dict = {'T': '10',
                       'J': '11',
                       'Q': '12',
                       'K': '13',
                       'A': '14'
                       }
 
        for index, card in enumerate(hand):
            if card[0] in letter_dict:
                new_card_number = letter_dict[card[0]]
                card_suit = card[1:]
                hand.append(new_card_number + card_suit)
      
        for card in hand:
            if card[0] == 'T' or card[0] == 'J' or card[0] == 'Q' or card[0] == 'K' or card[0] == 'A':
                pass
            else:
                hand_no_letters.append(card)
    
        for card in hand_no_letters:
            hand_tuples.append((card[0:-1], card[-1]))
      
        final_hand = sorted(hand_tuples, key=lambda x:int(x[0]))
      
        for card in final_hand:
            if card[0] not in hand_dict:
                hand_dict[card[0]] = [card[1]]
            else:
                hand_dict[card[0]].append(card[1])
  
        return (hand_dict, final_hand)

    
    def first_tiebreak_check(self, hand_score, other_score):
        if hand_score['score'] == 1 or hand_score['score'] == 5 or hand_score['score'] == 6 or hand_score['score'] == 9:
            length = 1
        elif hand_score['score'] == 2 or hand_score['score'] == 3:
            length = 2
        elif hand_score['score'] == 4:
            length = 3
        elif hand_score['score'] == 7:
            length = 3
        elif hand_score['score'] == 8:
            length = 4
        

         
        hand_tiebreaker = [key for key in hand_score['player_dict'] if len(hand_score['player_dict'][key]) == length]
        other_tiebreaker = [key for key in other_score['other_dict'] if len(other_score['other_dict'][key]) == length]

        if hand_score['score'] == 3 and other_score['score'] == 3:
            player_fifth_card = [key for key in hand_Score['player_dict'] if len(hand_score['player_dict'][key]) != length]
            h_tie_sort = sorted(hand_tiebreaker, key=lambda x:int(x))
            o_tie_sort = sorted(other_tiebreaker, key=lambda x:int(x))

            if int(h_tie_sort[1]) > int(o_tie_sort[1]):
                result = 'Win'
            elif int(h_tie_sort[1]) < int(o_tie_sort[1]):
                result = 'Loss'
            else:
                if player_fifth_card == other_fifth_card:
                    result = 'Tie'
                elif int(player_fifth_card) > int(other_fifth_card):
                    result = 'Win'
                elif int(player_fifth_card) < int(other_fifth_card):
                    result = 'Loss'

        # print 'hand tiebreaker', hand_tiebreaker
        for index, num in enumerate(hand_tiebreaker):
            if int(num) > int(other_tiebreaker[index]):
                result = 'Win'
                break
            elif int(num) < int(other_tiebreaker[index]):
                result = 'Loss'
                break
            else:
                player_tiebreak_list = [card[0] for card in sorted(hand_score['hand_data'], key=lambda x: int(x[0]), reverse=True) if card[0] != hand_tiebreaker]
                other_tiebreak_list = [card[0] for card in sorted(other_score['hand_data'], key=lambda x: int(x[0]), reverse=True) if card[0] != other_tiebreaker]
                result = self.tiebreak_edge_case(player_tiebreak_list, other_tiebreak_list)
                break
        return result

    
    def tiebreak_edge_case(self, player_tiebreak_list, other_tiebreak_list):
        if player_tiebreak_list == other_tiebreak_list:
            result = 'Tie'
        else:
            for index, num in enumerate(player_tiebreak_list):
                if int(num) == int(other_tiebreak_list[index]):
                    pass
                elif int(num) > int(other_tiebreak_list[index]):
                    result = 'Win'
                    break
                elif int(num) < int(other_tiebreak_list[index]):
                    result = 'Loss'
                    break

        return result


    def winner_result(self, hand_score, other_score):
        print 'hand_score', hand_score
        print 'other_score', other_score

        # Basic score check 
        if hand_score['score'] > other_score['score']:
            result = 'Win'
        elif hand_score['score'] < other_score['score']:
            result = 'Loss'
        elif hand_score['score'] == 10 and other_score['score'] == 10:
            result = 'Tie'
        else:
            result = self.first_tiebreak_check(hand_score, other_score)
        
        return result
      
    def compare_with(self, other):
      
        split_hand, split_other = self.hand.split(" "), other.hand.split(" ")
      
        hand_data, other_data = self.switch_letters(split_hand), self.switch_letters(split_other)
      
        player_dict, other_dict = hand_data[0], other_data[0]
        player_ordered, other_ordered = hand_data[1], other_data[1]
      
        player_pair, other_pair = False, False
        player_two_pair, other_two_pair = False, False
        player_three_of_kind, other_three_of_kind = False, False
        player_straight, other_straight = False, False
        player_flush, other_flush = False, False
        player_full_house, other_full_house = False, False
        player_four_of_kind, other_four_of_kind = False, False
        player_straight_flush, other_straight_flush = False, False
        player_royal_flush, other_royal_flush = False, False
      
        # High Card Check
        player_high_card, other_high_card = player_ordered[-1][0], other_ordered[-1][0]
      
        # Pair, Two-Pair, & Three-of-a-Kind Check
        player_pair_count, other_pair_count = 0, 0
      
        for key in player_dict:
            if len(player_dict[key]) == 2:
                player_pair_count += 1
                player_pair = True
            if len(player_dict[key]) == 3:
                player_three_of_kind = True
  
            if player_pair_count == 2:
                player_two_pair = True
        
        for key in other_dict:
            if len(other_dict[key]) == 2:
                other_pair_count += 1
                other_pair = True
            if len(other_dict[key]) == 3:
                other_three_of_kind = True
  
        if other_pair_count == 2:
            other_two_pair = True
    
        # Straight Check
        if int(player_ordered[0][0]) == int(player_ordered[1][0]) - 1 and int(player_ordered[1][0]) == int(player_ordered[2][0]) - 1 and int(player_ordered[2][0]) == int(player_ordered[3][0]) - 1 and int(player_ordered[3][0]) == int(player_ordered[4][0]) - 1:
            player_straight = True
        
        if int(other_ordered[0][0]) == int(other_ordered[1][0]) - 1 and int(other_ordered[1][0]) == int(other_ordered[2][0]) - 1 and int(other_ordered[2][0]) == int(other_ordered[3][0]) - 1 and int(other_ordered[3][0]) == int(other_ordered[4][0]) - 1:
            other_straight = True

        # Flush Check
        if player_ordered[0][1] == player_ordered[1][1] and player_ordered[1][1] == player_ordered[2][1] and player_ordered[2][1] == player_ordered[3][1] and player_ordered[3][1] == player_ordered[4][1]:
            player_flush = True
        
        if other_ordered[0][1] == other_ordered[1][1] and other_ordered[1][1] == other_ordered[2][1] and other_ordered[2][1] == other_ordered[3][1] and other_ordered[3][1] == other_ordered[4][1]:
            other_flush = True
  
        # Full House Check
        player_key_list = []
        other_key_list = []
  
        for key in player_dict:
            player_key_list.append(key)
    
        if len(player_dict) == 2:
            if len(player_dict[player_key_list[0]]) == 2 and len    (player_dict[player_key_list[1]]) == 3 or len    (player_dict[player_key_list[0]]) == 3 and len    (player_dict[player_key_list[1]]) == 2:
                player_full_house = True
          
        for key in other_dict:
            other_key_list.append(key)
    
        if len(other_dict) == 2:
            if len(other_dict[other_key_list[0]]) == 2 and len    (other_dict[other_key_list[1]]) == 3 or len    (other_dict[other_key_list[0]]) == 3 and len    (other_dict[other_key_list[1]]) == 2:
                other_full_house = True
    
        # Four-of-a-kind Check
        for key in player_dict:
            if len(player_dict[key]) == 4:
                player_four_of_kind = True
          
        for key in other_dict:
            if len(other_dict[key]) == 4:
                other_four_of_kind = True
  
        # Straight Flush Check
        if player_straight is True and player_flush is True:
            player_straight_flush = True
        if other_straight is True and other_flush is True:
            other_straight_flush = True 

        # Royal Flush Check
        if player_straight_flush is True and player_ordered[-1][0] == '14':
            player_royal_flush = True
        if other_straight_flush is True and other_ordered[-1][0] == '14':
            other_royal_flush = True
        
        # Assign a score according to the hand's highest value combination
        player_score = 0
        other_score = 0
  
        if player_royal_flush is True:
            player_score = 10
        elif player_straight_flush is True:
            player_score = 9
        elif player_four_of_kind is True:
            player_score = 8
        elif player_full_house is True:
            player_score = 7
        elif player_flush is True:
            player_score = 6
        elif player_straight is True:
            player_score = 5
        elif player_three_of_kind is True:
            player_score = 4
        elif player_two_pair is True:
            player_score = 3
        elif player_pair is True:
            player_score = 2
        else:
            player_score = 1
        
        if other_royal_flush is True:
            other_score = 10
        elif other_straight_flush is True:
            other_score = 9
        elif other_four_of_kind is True:
            other_score = 8
        elif other_full_house is True:
            other_score = 7
        elif other_flush is True:
            other_score = 6
        elif other_straight is True:
            other_score = 5
        elif other_three_of_kind is True:
            other_score = 4
        elif other_two_pair is True:
            other_score = 3
        elif other_pair is True:
            other_score = 2
        else:
            other_score = 1
        
        player_score_dict = {'score': player_score,
            'player_dict': player_dict,
            'high_card': player_high_card,
            'hand_data': player_ordered
                            }
      
        other_score_dict = {'score': other_score,
            'other_dict': other_dict,
            'high_card': other_high_card,
            'hand_data': other_ordered
                           }
      
        return self.winner_result(player_score_dict, other_score_dict)


player = PokerHand("4C 5C 9C 8C KC")
other = PokerHand("3S 8S 9S 5S KS")
print player.compare_with(other)

# 1 - high card
# 2 - pair
# 3 - 2 pair
# 4 - 3 of kind
# 5 - straight
# 6 - flush
# 7 - full house
# 8 - four of kind
# 9 - straight flush
# 10 - royal flush