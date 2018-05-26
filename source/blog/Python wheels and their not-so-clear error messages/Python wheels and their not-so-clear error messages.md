<!-- ## BEGIN METADATA ##
title:: So, you can't install that wheel, huh?
date:: April 26 2018
## END METADATA ## -->

# So, you can't install that wheel, huh?

In particular, say you're trying to install a package and you get an error like:

```
> pip install tensorflow

Could not find a version that satisfies the requirement tensorflow (from versions: )
No matching distribution found for tensorflow
```

(You may guess which package was giving me trouble.) You go straight to PyPI, link/download your specific OS version (in my case, amd64):

```
> pip install --upgrade https://files.pythonhosted.org/packages/35/f6/8af765c7634bc72a902c50d6e7664cd1faac6128e7362510b0234d93c974/tensorflow-1.7.0-cp36-cp36m-win_amd64.whl

tensorflow-1.7.0-cp36-cp36m-win_amd64.whl is not supported wheel on this platform
```


Then you give up and choose the most generic option to make the errors stop:

```
> pip install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.7.0-py3-none-any.whl

Installing collected packages: ...
```

Finally, it installs! (You may already notice something funny, but let's press on.) You go to verify it installed correctly:

```
> python

Python 3.6.5 ...
Type "help", "copyright", "credits" or "license" for more information.
>>> import tensorflow as tf
...
ImportError: cannot import name pywrap_tensorflow
```

You can't believe it! Checking online, you see that you may need MSVCP140.DLL in your PATH -- yup, it's there. No other troubleshooting suggestions! You wonder and wonder, when suddenly it becomes clear.

## pip doesn't really care what OS you're running.
What it cares about is your *Python* version.

Which, yes, cares about what OS you're running. But when pip is checking whether a wheel is supported on a platform (e.g. "win_amd64"), it's curious about:

> Python 3.6.5 (...) [***MSC v.1900 64 bit (AMD64)***] on win32

Which, as you may have guessed, was not amd64 when I ran the above pip commands. I'm not entirely sure why I had the 32-bit version of Python installed as default, but it isn't the case anymore. Though I suppose a fun fact was learned: the Tensorflow wheel meant only to be used as a last resort for Mac OSX users (hence "/mac/" in the none-any.whl path) can be installed on any OS, a fact which will eventually lead to further levels of confusion.

Finally, with this revelation and a few installs, we get:

```
> pip install tensorflow

Installing collected packages: ...
[...]
>
> python
Python 3.6.5 ...
Type "help", "copyright", "credits" or "license" for more information.
>>> import tensorflow as tf
>>>
```

Huzzah!

\- DK, 4/26/18