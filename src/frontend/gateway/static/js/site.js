require('../css/style.css');

import ReactDOM from 'react-dom';
import React from 'react';
import CheckoutForm from './components/CheckoutForm.jsx';
import RecentDonations from './components/RecentDonations.jsx';
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
        ReactDOM.render((
            <RecentDonations n={5} />
        ), recentDonations);
    }
}());

