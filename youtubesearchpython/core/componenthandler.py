from typing import Union, List


def getValue(source: dict, path: List[str]) -> Union[str, int, dict, None]:
    value = source
    for key in path:
        if type(key) is str:
            if key in value.keys():
                value = value[key]
            else:
                value = None
                break
        elif type(key) is int:
            if len(value) != 0:
                value = value[key]
            else:
                value = None
                break
    return value


def getVideoId(videoLink: str) -> str:
    if 'youtu.be' in videoLink:
        # Extract the path part and remove query parameters
        path_part = videoLink.split('?')[0].split('#')[0]
        if path_part[-1] == '/':
            return path_part.split('/')[-2]
        return path_part.split('/')[-1]
    elif 'youtube.com' in videoLink:
        # Extract video ID from v= parameter, handling query parameters
        if 'v=' in videoLink:
            v_index = videoLink.index('v=') + 2
            # Find the end of the video ID (either &, #, or end of string)
            end_index = len(videoLink)
            for char in ['&', '#']:
                if char in videoLink[v_index:]:
                    end_index = min(end_index, videoLink.index(char, v_index))
            return videoLink[v_index:end_index]
        return videoLink
    else:
        return videoLink

