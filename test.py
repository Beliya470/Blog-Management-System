def solution(S):
    # Initialize the number of patches applied to 0.
    patches = 0
    
    # Initialize the current position in the string S to 0.
    i = 0
    
    # Get the length of the road segments.
    N = len(S)
    
    # Go through all the segments of the road.
    while i < N:
        # If there is a pothole in the current segment.
        if S[i] == 'X':
            # Apply a patch and increment the patches counter.
            patches += 1
            
            # Skip the next two segments, as they're covered by the current patch.
            i += 3
        else:
            # If the current segment doesn't have a pothole, move to the next segment.
            i += 1
    
    # Return the total number of patches applied.
    return patches
