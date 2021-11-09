from Point import Point, do_intersect


def evaluate_movement(current_data, prev_data):
    print('Running Eval')
    EMAP3 = Point(prev_data['Unix Timestamp'], prev_data['3 Period EMA'])
    EMAQ3 = Point(current_data['Unix Timestamp'], current_data['3 Period EMA'])
    EMAP6 = Point(prev_data['Unix Timestamp'], prev_data['6 Period EMA'])
    EMAQ6 = Point(current_data['Unix Timestamp'], current_data['6 Period EMA'])
    EMAP9 = Point(prev_data['Unix Timestamp'], prev_data['9 Period EMA'])
    EMAQ9 = Point(current_data['Unix Timestamp'], current_data['9 Period EMA'])

    if do_intersect(EMAP3, EMAQ3, EMAP6, EMAQ6) or do_intersect(EMAP3, EMAQ3, EMAP9, EMAQ9):
        print('3P EMA intersected with 6P EMA')
        if current_data['3 Period EMA'] > prev_data['6 Period EMA']:
            print("3P EMA is above 6P EMA")
        if current_data['3 Period EMA'] < prev_data['6 Period EMA']:
            print("3P EMA is below 6P EMA")
        if current_data['3 Period EMA'] > prev_data['9 Period EMA']:
            print("3P EMA is above 9P EMA")
        if current_data['3 Period EMA'] < prev_data['9 Period EMA']:
            print("3P EMA is below 9P EMA")
        # Check if the 3 Period EMA is going below the 6 and 9 Period EMA
        # Also check if the last two candles are bearish
        # If both are the case, it's a good time to sell
        if current_data['3 Period EMA'] < prev_data['9 Period EMA'] \
                and current_data['3 Period EMA'] < prev_data['6 Period EMA']:
            # and current_data['Description'] == 'Bearish' \
            # and prev_data['Description'] == 'Bearish':
            print('3EMA Going BELOW 6EMA and 9EMA - SELL')
            return 'SELL'
        # Check if the 3 Period EMA is going above the 6 and 9 Period EMA
        # Also check if the last two candles are bullish
        # If both are the case, it's a good time to buy
        if current_data['3 Period EMA'] > prev_data['9 Period EMA'] \
                and current_data['3 Period EMA'] > prev_data['6 Period EMA']:
            # and current_data['Description'] == 'Bullish' \
            # and prev_data['Description'] == 'Bullish':
            print('3EMA Going ABOVE 6EMA and 9EMA - BUY')
            return 'BUY'
