> Todo:
>
>       [X] Add nahayatnegar market map to jobs
>
>       [X] Setup selenium to select filters in nahayatnegar

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

> Fix:
>
>       [X] Passing actual login_required value to take_screenshot()
>
>       [X] Print batch_runner log in console supporting tuple format
>
>       [ ] Image index 4 & 5 & 6 in livetse site
>
>       [X] Function sleep() in take_screenshot() should run once for each driver session

> Note:
>
>       - Option "headless" is disabled in take_screenshot()
>
>       - Module driver.quit() replaced by closing from contextlib
