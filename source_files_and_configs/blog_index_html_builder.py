# Website HTML builder
# To be run ***offline*** (and later served by nginx via try_files)


# website_root = '/home/davogk/personal-website'
website_root = '.' # root handled by server already (?)

def head(website_loc):
    """
    Return the head of the HTML doc,
    with website_loc as the start of the page's title.
    """
    head = """  <head>


    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="David G. Khachatrian">
    <!-- <link rel="icon" href="http://getbootstrap.com/docs/3.3/favicon.ico"> -->

    <title>{0} - davidkhachatrian.com</title>

    <!-- Bootstrap core CSS -->
    <link href="./css/bootstrap.min.css" rel="stylesheet">

    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <link href="./css/ie10-viewport-bug-workaround.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="./css/cover.css" rel="stylesheet">


    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  """
  return head.format(website_loc)

