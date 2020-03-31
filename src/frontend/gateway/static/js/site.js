require('../css/style.css');

import ReactDOM from 'react-dom';
import React from 'react';
import CheckoutForm from './components/CheckoutForm.jsx';
import RecentDonations from './components/RecentDonations.jsx';
import TeamStats from './components/TeamStats.jsx';
import DonationStats from './components/DonationStats.jsx';
import config from './config.js';

(function() {
    const donationForm = document.getElementById('donation-form');
    if (donationForm) {
        ReactDOM.render((
            <CheckoutForm stripeKey={config.STRIPE_PUBLIC_KEY} />
        ), donationForm);
    }

    const recentDonations = document.getElementById('recent-donations');
    if (recentDonations) {
        async function getDonations() {
            const response = await fetch(`/recent-donations/?n=5`, {
                method: 'GET',
                headers: {
                    'Accepts': 'application/json',
                }
            });
            const { data } = await response.json();

            ReactDOM.render((
                <RecentDonations donations={data} />
            ), recentDonations);
        }

        getDonations();
        // refresh donation list every 5s
        setInterval(getDonations, 5000);
    }

    const teamStats = document.getElementById('folding-team-stats');
    if (teamStats) {
        ReactDOM.render((
            <TeamStats donationCount={window.FOLD.DONATION_COUNT} />
        ), teamStats);
    }

    const donationStats = document.getElementById('folding-donation-stats');
    if (donationStats) {
        ReactDOM.render((
            <DonationStats donationId={window.FOLD.DONATION_ID} initialDonationAmount={window.FOLD.DONATION_AMOUNT} />
        ), donationStats);
    }
}());

