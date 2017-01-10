import re, emoji

TEST_STRINGS = ['Lorem ipsum netus porta fames faucibus nec nostra, molestie consequat himenaeos faucibus leo sed, id velit ut curabitur id ligula.',
               'Justo lacinia erat eros sociosqu porttitor lacinia malesuada mollis tempus, tortor mauris molestie luctus morbi justo sem conubia, ut ornare gravida venenatis fames semper senectus ante.',
               'Imperdiet convallis felis tempus orci porta tortor suspendisse lobortis dictumst, nulla ligula varius ut aliquam ac justo adipiscing dolor potenti, magna accumsan dictumst non consectetur laoreet phasellus eleifend adipiscing quisque a litora convallis egestas.',
               'Tincidunt felis purus quis dictumst luctus convallis ut dapibus platea, eleifend vel euismod ante pellentesque ornare arcu praesent, adipiscing hac ornare eu himenaeos sapien enim platea.',
               'At nam faucibus ultrices varius laoreet pellentesque pharetra sem neque, mi aliquam feugiat varius nibh et viverra sed, conubia dictum tincidunt lobortis massa suspendisse elementum imperdiet.']

def validate_regex(regex, case_sensitive):
    try:
        compiledre = re.compile(emoji.emojize(regex, True), 0 if case_sensitive else re.IGNORECASE)
    except:
        return 'Couldn\'t compile regex %s!' % regex
    foundCount = 0
    for s in TEST_STRINGS:
        if compiledre.search(s) != None:
            foundCount += 1
    if foundCount > 1:
        return 'The regex %s matches too often' % regex
    return compiledre