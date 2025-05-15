> Todo:
>
>       [X] Add nahayatnegar market map to jobs
>
>       [X] Setup selenium to select filters in nahayatnegar
>
>       [X] Add LiveTSE blog texts as template
>
>       [ ] Implementing a text content update system
>
>       [X] Implementing image merging capability
>
>       [ ] Add jinja2 notations to blog template
>
>       [ ] Implement work date calculator system and add it to report_exporter.py

> Feture:
>
>       [X] Implement valid_inputs() for take_screenshot()
>
>       [X] Add data type check for take_screenshot function in screenshot.py
>
>       [ ] Add auto path logic if one path and multiple indexes given

> Improvement:
>
>       [ ] Improve logger.py logging messages to show success status
>
>       [ ] Replace sleep() with wait() for element in capture_element()
>
>       [ ] Add try, except for login_livetse()
>
>       [ ] Add index to multi screenshot log in batch_runner.py for better readability
>
>       [ ] Add url (the name in the url) to default path while saving image in batch_runner.py
>
>       [ ] Crop LiveTSE image paddings
>
>       [ ] Package tools
>
>       [ ] Add input validation and try-except to merge_images_with_gap()
>
>       [ ] Improve print statements in batch_runner.py and pass messages to print_console()

> Fix:
>
>       [X] Passing actual login_required value to take_screenshot()
>
>       [X] Print batch_runner log in console supporting tuple format
>
>       [X] Image index 4 & 5 & 6 in LiveTSE web site
>
>       [X] Function sleep() in take_screenshot() should run once for each driver session

> Note:
>
>       - Option "headless" is disabled in take_screenshot()
>
>       - Module driver.quit() replaced by closing from contextlib
>
>       - Option 'timeout' is implemented in take_screenshot() but it's not supported by batch_runner.py 
