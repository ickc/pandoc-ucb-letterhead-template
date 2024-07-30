---
title: UCB Letterhead
author: Firstname Lastname
date: \today
papersize:    letter
fontsize:    12pt
documentclass:    letter
geometry:
    - inner=1in
    - outer=1in
    - top=1in
    - bottom=1in
mainfont: UCBerkeleyOS.otf
mainfontoptions:
    - BoldFont=UCBerkeleyOSBold.otf
    - ItalicFont=UCBerkeleyOSItalic.otf
    - BoldItalicFont=UCBerkeleyOSBoldItalic.otf
ucb-letterhead:
    lfoot: Letter from Firstname Lastname regarding ...
    cfoot:
    title: Title
    department: Department
    address: Address
    address2: Berkeley CA, 94720
    email: username@berkeley.edu
    phone: (510) 642--0000
    mobile: (510) XXX--XXXX
    url: https://*.berkeley.edu
    recipient: |
        ```{=latex}
        Recipient name \\ Street\\ City\\ Country \\ [\parskip]
        Re:
        ```
header-includes: |
    ```{=latex}
    \usepackage{lipsum} %you can delete this
    ```
---

\opening{Dear Professor Recipient Name,}

Replace these contents with your own!

<!-- erase this to remove placeholder text -->
\lipsum[1-3]

<!-- use this command to break to page 2. It's included here so that the margins will be different on pages 2+ -->
\newpage

<!-- page dimensions for page 2+ -->
\newgeometry{top=1in,bottom=1in,right=1in,left=1in}

**Feel free to use**

-   bullets

1.  numbered lists

2.  numbered lists interrupted by bullets

    -   A bullet between numbers

3.  Yes, anything is possible

*The quote command:*

> Hello my friend, we've been waiting for you for a long time\
> We have reason to believe that your soul is just like ours\
> Did you ever get the feeling you were just a little different?\
> Well, here's our web page, you've finally found a home

***The verse command:***

> As for me, I am light and joyous! I discover in men dazzling
> perspectives, with Paradises in the clouds and distant felicities. I
> pour into their souls the eternal insanities, projects of happiness,
> plans for the future, dreams of glory, and oaths of love, as well as
> virtuous resolutions. I drive them on perilous voyages and on mighty
> enterprises. I have carved with my claws the marvels of architecture.
> It is I that hung the little bells on the tomb of Porsenna, and
> surrounded with a wall of Corinthian brass the quays of the
> Atlantides.
>
> I seek fresh perfumes, larger flowers, pleasures hitherto unknown. If
> anywhere I find a man whose soul reposes in wisdom, I fall upon him
> and strangle him.

```{=tex}
\closing{Sincerely,}

Firstname Lastname


\ps{P.S. Fiat Lux}

\cc{Carbon Copy 1\\Carbon Copy 2}

\encl{Memorandum}
```
