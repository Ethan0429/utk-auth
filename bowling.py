from dataclasses import dataclass


@dataclass
class Frame:
    first_roll: int = 0
    second_roll: int = 0
    third_roll: int = 0
    strike: bool = False
    spare: bool = False


# n = [8, 0, 1, 9, 4, 0, 9, 9, 10, 9, 1, 4, 2, 0, 3, 5, 5, 9, 1, 8]
n = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
     10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
frames = []

# input is in the form of "10 10 10 10 10 10 10 10 10 10 10 10"
# step through the list in increments of 2
for i in range(0, len(n), 2):
    # if the first roll is 10, it's a strike
    if n[i] == 10:
        frames.append(Frame(first_roll=n[i], strike=True))
    # if the second roll is 10, it's a spare
    elif n[i] + n[i + 1] == 10:
        frames.append(Frame(first_roll=n[i], second_roll=n[i + 1], spare=True))
    # otherwise it's a normal frame
    else:
        frames.append(Frame(first_roll=n[i], second_roll=n[i + 1]))

if len(n) == 21:
    frames[-1].third_roll = n[20]

# print the frames
for frame in frames:
    print(frame)

# print the scores
final_score = 0
for i in range(len(frames)):
    # if it's the last frame, just add the two rolls
    if i == 9:
        final_score += frames[i].first_roll + \
            frames[i].second_roll + frames[i].third_roll
        break
    # if the frame is a strike, add the next two rolls
    if frames[i].strike:
        # if the next frame is a strike, add the next two rolls
        if frames[i + 1].strike:
            final_score += frames[i].first_roll + \
                frames[i + 1].first_roll + frames[i + 2].first_roll
        # otherwise just add the next two rolls
        else:
            final_score += frames[i].first_roll + \
                frames[i + 1].first_roll + frames[i + 1].second_roll
    # if the frame is a spare, add the next roll
    elif frames[i].spare:
        final_score += frames[i].first_roll + \
            frames[i].second_roll + frames[i + 1].first_roll
    # otherwise just add the two rolls
    else:
        final_score += frames[i].first_roll + frames[i].second_roll

print(final_score)
