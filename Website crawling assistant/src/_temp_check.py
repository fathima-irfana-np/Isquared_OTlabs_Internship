"""Check Click 'x' usage in spec."""
lines = open("specs/ai_exploration.spec", "r", encoding="utf-8").readlines()

# Count Click 'x' occurrences
click_x = [l.strip() for l in lines if l.strip() == "* Click 'x'"]
total_scenarios = sum(1 for l in lines if l.startswith("## "))
print("Click 'x' occurrences:", len(click_x), "out of", total_scenarios, "scenarios")
print()

# All unique Click steps with counts
clicks = {}
for l in lines:
    l = l.strip()
    if l.startswith("* Click"):
        clicks[l] = clicks.get(l, 0) + 1

print("All unique Click steps:")
for c, n in sorted(clicks.items(), key=lambda x: -x[1]):
    print(f"  [{n}x] {c}")
