def analizeAnnotated(fn):
    blinks = [[float(y) for y in x.split(",") if y != "p"] for x in file("annotations/"+fn, "rb").read().strip().split("\n")]
    for blink in blinks:
        print blink[1]-blink[0], blink[2]-blink[0], repr(blink)
    #print blinks
    return




if __name__ == "__main__":
    analizeAnnotated("o90")
