#!/bin/sh

VERSION=`cat VERSION`
INS_PATH=/usr

# Checking whether 'festival' is installed or not
which festival > /dev/null 2>&1
if [ $? == 0 ];then
	echo -n ""
else
	echo "Please install 'festival' package, otherwise Swaram will not work."
fi

# Checking whether 'sox' is installed or not
which play > /dev/null 2>&1
if [ $? == 0 ];then
	echo -n ""
else
	echo "Please install 'sox' package, otherwise Swaram will not work."
fi

# Checking whether 'xpdf' is installed or not
which pdftotext > /dev/null 2>&1
if [ $? == 0 ];then
	echo -n ""
else
	echo "Please install 'xpdf' package, otherwise PDF files cannot play."
fi

# Checking whether 'lynx' is installed or not
which lynx > /dev/null 2>&1
if [ $? == 0 ];then
	echo -n ""
else
	echo "Please install 'lynx' package, otherwise HTML files cannot play."
fi

# Installing the basic stuff
mkdir -p $INS_PATH/share/swaram
cp -f swaram swaram.glade swaram.py swaramBase.py mainWindow.py prefWindow.py messageDialog.py swaram.xpm nt2w $INS_PATH/share/swaram
ln -sf $INS_PATH/share/swaram/swaram $INS_PATH/bin/swaram
ln -sf $INS_PATH/share/swaram/nt2w $INS_PATH/bin/nt2w

# Installing swaram.desktop , swaram.png and swaram.conf
cp -f swaram.desktop $INS_PATH/share/applications/swaram.desktop
cp -f swaram.png $INS_PATH/share/pixmaps/swaram.png
cp -f swaram.conf /etc/swaram.conf

# Installing doc files
mkdir -p $INS_PATH/share/doc/swaram-$VERSION
cp -f COPYING FAQ README ChangeLog TODO $INS_PATH/share/doc/swaram-$VERSION
