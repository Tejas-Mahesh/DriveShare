document.addEventListener("DOMContentLoaded", function () {

    // -------------------------
    // Booking Chart
    // -------------------------
    
    const bookingLabelsElement =
        document.getElementById("booking-labels");

    const bookingCountsElement =
        document.getElementById("booking-counts");
    

    if (bookingLabelsElement && bookingCountsElement) {

        const bookingLabels =
            JSON.parse(bookingLabelsElement.textContent);

        const bookingCounts =
            JSON.parse(bookingCountsElement.textContent);

        const bookingCanvas =
            document.getElementById("bookingChart");

        if (bookingCanvas) {

            new Chart(bookingCanvas, {

                type: "line",

                data: {

                    labels: bookingLabels,

                    datasets: [{

                        label: "Bookings",

                        data: bookingCounts,

                        borderWidth: 3,

                        tension: 0.4,

                        fill: false

                    }]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false

                }

            });

        }

    }

    // -------------------------
    // Revenue Chart
    // -------------------------

    const revenueLabelsElement =
        document.getElementById("revenue-labels");

    const revenueValuesElement =
        document.getElementById("revenue-values");

    if (revenueLabelsElement && revenueValuesElement) {

        const revenueLabels =
            JSON.parse(revenueLabelsElement.textContent);

        const revenueValues =
            JSON.parse(revenueValuesElement.textContent);

        const revenueCanvas =
            document.getElementById("revenueChart");

        if (revenueCanvas) {

            new Chart(revenueCanvas, {

                type: "bar",

                data: {

                    labels: revenueLabels,

                    datasets: [{

                        label: "Revenue",

                        data: revenueValues,

                        borderWidth: 2

                    }]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false

                }

            });

        }

    }

});

const paymentCtx = document.getElementById("paymentStatusChart");

if (paymentCtx) {

    new Chart(paymentCtx, {

        type: "pie",

        data: {

            labels: paymentStatusLabels,

            datasets: [{

                data: paymentStatusData

            }]

        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    position: "bottom"

                }

            }

        }

    });

}