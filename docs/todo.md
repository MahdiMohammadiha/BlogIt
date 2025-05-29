> Todo:
>
>       [X] Add nahayatnegar market map to jobs
>
>       [X] Setup selenium to select filters in nahayatnegar
>
>       [X] Add LiveTSE blog texts as template
>
>       [X] Implementing a text content update system
>
>       [X] Implementing image merging capability
>
>       [X] Add jinja2 notations to blog template
>
>       [ ] Implement work date calculator system and add it to report_exporter.py
>
>       [X] Add 2nd report extractor for LiveTSE notifications
>
>       [ ] Implement a root point like main.py for project execution flow
>
>       [ ] Implement auto media upload system
>
>       [ ] Implement auto blog system for WP
>
>       [ ] Add banner image creator function
>
>       [ ] Add watchlist table generator module
>
>       [ ] Implement error detection and skip error system

> Feture:
>
>       [X] Implement valid_inputs() for take_screenshot()
>
>       [X] Add data type check for take_screenshot function in screenshot.py
>
>       [ ] Add auto path logic if one path and multiple indexes given
>
>       [X] Implement image scale feature for smaller scales in blog.html
>
>       [ ] Separating selenium tools into a package
>
>       [ ] Integration of web driver waits
>
>       [ ] Implement minimalize html module for perfomance enhancement
>
>       [ ] Implement retry system for errors

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
>
>       [X] Fix screenshots from LiveTSE charts when --headless option is disabled
>
>       [ ] Fix img html style for LiveTSE images

> Note:
>
>       - Module driver.quit() replaced by closing from contextlib
>
>       - Option 'timeout' is implemented in take_screenshot() but it's not supported by batch_runner.py 
