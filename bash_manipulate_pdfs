#!/usr/bin/env bash
FILENAME="$1"
PRINTER="CHANGE THIS TO THE PRINTER NAME"
echo "Working on file $FILENAME."
COUNT="$(pdfcount ${FILENAME})"
DEST="${FILENAME}_tmp_"

if [ "$COUNT" = 3 ] ; then
		echo "Sending page 3 to printer..."
		pdfsplit $FILENAME 3 |lpr -P $PRINTER
		echo "Removing printed page from document."
		pdfsplit $FILENAME 1-2 >"$DEST"
elif [ "$COUNT" = 6 ] ; then
		echo "Sending pages 3 and 6 to printer..."
                pdfsplit $FILENAME 3 6 |lpr -P $PRINTER
                echo "Removing printed pages from document."
                pdfsplit $FILENAME 1-2 4-5 > "$DEST"
elif [ "$COUNT" = 9 ] ; then
                echo "Sending pages 3, 6 and 9 to printer..."
                pdfsplit $FILENAME 3 6 9 |lpr -P $PRINTER
                echo "Removing printed pages from document."
                pdfsplit $FILENAME 1-2 4-5 7-8 > "$DEST"
elif [ "$COUNT" = 12 ] ; then
                echo "Sending pages 3, 6, 9 and 12 to printer..."
                pdfsplit $FILENAME 3 6 9 12 |lpr -P $PRINTER
                echo "Removing printed pages from document."
                pdfsplit $FILENAME 1-2 4-5 7-8 10-11 > "$DEST"
elif [ "$COUNT" = 15 ] ; then
                echo "Sending pages 3, 6, 9, 12 and 15 to printer..."
                pdfsplit $FILENAME 3 6 9 12 15 |lpr -P $PRINTER
                echo "Removing printed pages from document."
                pdfsplit $FILENAME 1-2 4-5 7-8 10-11 13-14> "$DEST"
elif [ "$COUNT" = 18 ] ; then
                echo "Sending pages 3, 6, 9, 12, 15 and 18 to printer..."
                pdfsplit $FILENAME 3 6 9 12 15 18 |lpr -P $PRINTER
                echo "Removing printed pages from document."
                pdfsplit $FILENAME 1-2 4-5 7-8 10-11 13-14 16-17> "$DEST"
else
		echo "Don't you agree that you're going nuts about the number of pages in that document?..."
fi

echo "Deleting the original file ($FILENAME)."
rm $FILENAME
echo "Renaming new document to the original filename ($FILENAME)"
mv $DEST $FILENAME
echo "Done."
