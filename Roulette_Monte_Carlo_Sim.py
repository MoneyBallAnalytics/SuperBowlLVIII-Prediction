import random
import matplotlib.pyplot as plt

def spin_roulette():
    """Simulates a spin of a roulette wheel."""
    number = random.randint(0, 37)  # 37 represents 00
    if number == 0:
        return "green", 0
    elif number == 37:
        return "green", "00"
    elif number <= 18:
        return "red", number
    else:
        return "black", number

def play_roulette(max_spins=10, ante=1):
    """
    Simulates a single roulette game with a maximum number of spins,
    random bet types and amounts, and an ante fee.
    """
    balance = 100
    num_spins = 0

    while balance >= 5 and num_spins < max_spins:
        balance -= ante
        # print(f"Your current balance is ${balance}")  # Removed print statement

        bet_type = random.choice(['n', 'c', 'b'])

        if bet_type == 'n':
            bet_number = random.randint(1, 36)
            bet_amount = random.randint(5, max(5, min(balance, 10)))  # Ensure bet_amount is at least 5
            result_color, result_number = spin_roulette()
            if bet_number == result_number:
                balance += bet_amount * 35
            else:
                balance -= bet_amount

        elif bet_type == 'c':
            bet_color = random.choice(["red", "black"])
            bet_amount = random.randint(5, max(5, min(balance, 20)))  # Ensure bet_amount is at least 5
            result_color, result_number = spin_roulette()
            if bet_color == result_color:
                balance += bet_amount
            else:
                balance -= bet_amount

        else:  # bet_type == 'b'
            bet_number = random.randint(1, 36)
            bet_color = random.choice(["red", "black"])
            bet_amount_number = random.randint(5, max(5, min(balance // 2, 10)))  # Ensure bet_amount is at least 5
            bet_amount_color = random.randint(5, max(5, min(balance // 2, 20)))  # Ensure bet_amount is at least 5
            result_color, result_number = spin_roulette()
            if bet_number == result_number:
                balance += bet_amount_number * 35
            else:
                balance -= bet_amount_number
            if bet_color == result_color:
                balance += bet_amount_color
            else:
                balance -= bet_amount_color

        num_spins += 1  # Increment num_spins after each spin

    return balance

def monte_carlo_simulation(num_simulations, max_spins=10, ante=1):
    """
    Runs a Monte Carlo simulation of the roulette game with and without ante.
    """
    ending_balances_with_ante = []
    ending_balances_no_ante = []
    total_winnings_with_ante = 0  # Track casino winnings with ante
    total_winnings_no_ante = 0  # Track casino winnings without ante

    for _ in range(num_simulations):
        ending_balance_with_ante = play_roulette(max_spins, ante)  # Use max_spins instead of min_bets
        ending_balances_with_ante.append(ending_balance_with_ante)
        total_winnings_with_ante += 100 - ending_balance_with_ante + (ante * max_spins)  # Calculate casino winnings

        ending_balance_no_ante = play_roulette(max_spins, ante=0)  # Simulate without ante
        ending_balances_no_ante.append(ending_balance_no_ante)
        total_winnings_no_ante += 100 - ending_balance_no_ante  # Calculate casino winnings

    # Analyze results
    avg_ending_balance_with_ante = sum(ending_balances_with_ante) / num_simulations
    win_probability_with_ante = sum(1 for balance in ending_balances_with_ante if balance > 100) / num_simulations
    loss_probability_with_ante = 1 - win_probability_with_ante

    avg_ending_balance_no_ante = sum(ending_balances_no_ante) / num_simulations
    win_probability_no_ante = sum(1 for balance in ending_balances_no_ante if balance > 100) / num_simulations
    loss_probability_no_ante = 1 - win_probability_no_ante

    print("With Ante:")
    print(f"Average ending balance: ${avg_ending_balance_with_ante:.2f}")
    print(f"Win probability: {win_probability_with_ante:.2%}")
    print(f"Loss probability: {loss_probability_with_ante:.2%}")

    print("\nWithout Ante:")
    print(f"Average ending balance: ${avg_ending_balance_no_ante:.2f}")
    print(f"Win probability: {win_probability_no_ante:.2%}")
    print(f"Loss probability: {loss_probability_no_ante:.2%}")

    # Visualize results
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)  # Create two subplots
    plt.hist(ending_balances_with_ante, bins=20)
    plt.xlabel("Ending Balance (with ante)")
    plt.ylabel("Frequency")
    plt.title("Distribution with Ante")

    plt.subplot(1, 2, 2)
    plt.hist(ending_balances_no_ante, bins=20)
    plt.xlabel("Ending Balance (no ante)")
    plt.ylabel("Frequency")
    plt.title("Distribution without Ante")

    plt.tight_layout()  # Adjust spacing between subplots
    plt.show()

    # Print total casino winnings
    print(f"Total casino winnings with ante: ${total_winnings_with_ante:.2f}")
    print(f"Total casino winnings without ante: ${total_winnings_no_ante:.2f}")

if __name__ == "__main__":
    num_simulations = 10000
    monte_carlo_simulation(num_simulations)