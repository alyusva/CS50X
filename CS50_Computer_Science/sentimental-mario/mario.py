def get_height():
    while True:
        try:
            height = int(input("Height: "))
            if 1 <= height <= 8:
                return height
        except ValueError:
            pass

def print_pyramids(height):
    for i in range(1, height + 1):
        # Left pyramid
        left_pyramid = ' ' * (height - i) + '#' * i
        # Right pyramid
        right_pyramid = '#' * i
        # Two spaces between pyramids
        print(f"{left_pyramid}  {right_pyramid}")

def main():
    height = get_height()
    print_pyramids(height)

if __name__ == "__main__":
    main()
