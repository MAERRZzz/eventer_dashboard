document.addEventListener("DOMContentLoaded", function () {
            function nameLimit(venueName, maxLength) {
                if (venueName.length <= maxLength) {
                    return venueName;
                } else {
                    return venueName.slice(0, maxLength) + '...';
                }
            }

            const venues = document.getElementsByClassName('venueName');

            for (let i = 0; i < venues.length; i++) {
                const venueName = venues[i].innerHTML;
                venues[i].innerHTML = nameLimit(venueName, 25);
            }
        }
    )