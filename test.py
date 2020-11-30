def bestFlush(holeCards, communityCards=list())
    cards = sorted(list(holeCards) + communityCards)
    rankCount = dict()
    suitCount = dict()
    for card in cards:
        rankCount[card.rank] = rankCount.get(card.rank, 0) + 1
        suitCount[card.suit] = rankCount.get(card.suit, 0) + 1
    
    flush_suit = max(suitCount)
    if suitCount[flush_suit] >= 5:
        for card in range(1, len(cards)):
            if card.suit == flush_suit and 


def bestStraight(holeCards, communityCards=list()):
    cards = sorted(list(holeCards) + communityCards)
    bestHand = [cards[0]]
    for i in range(1, len(cards)):
        if cards[i-1].rank + 1 == cards[i].rank:
            bestHand.append(cards[i])
        elif 