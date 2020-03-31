import React from 'react';
import { useState } from 'react';
import Stat from './Stat.jsx';
import config from "../config";

const DonationStats = ({ donationId, initialDonationAmount }) => {
    const [donationData, setDonationData] = useState({});

    (async function retrieveDonationData() {
        const statusEndpoint = `${config.STATUS_API}/prod/donations/${donationId}`;
        const donation = await fetch(statusEndpoint, {
            method: 'GET'
        });
        const { data } = await donation.json();

        setDonationData(data);
    }());

    let stats = [];
    if (donationData.canonical_status) {
        stats = [
            {
                title: 'Status',
                label: 'the current processing status of the donation',
                value: `${donationData.canonical_status}`
            },
            {
                title: "Amount",
                label: "the amount donated",
                value: initialDonationAmount
            },
            {
                title: 'Amount Remaining',
                label: 'the amount of the initial donation not yet used in solving',
                value: `$${donationData.balance_remaining / 100}`
            },
        ];
    }
    return (
        <div className="flex flex-col lg:flex-row items-start w-full sm:w-3/4 lg:w-full">
            {stats.length > 0 ? stats.map((s, ix) => {
                let classes = ['py-4', 'lg:py-0', 'px-2', 'md:px-8', 'my-4', 'lg:my-0', 'border', 'border-gray-100', 'lg:border-none', 'shadow-lg', 'lg:shadow-none', 'mx-0', 'lg:mx-4'];
                if (ix === 0) {
                    classes = classes.concat(['lg:ml-0', 'lg:pl-0']);
                }

                return (
                    <div className={classes.join(' ')}>
                        <Stat title={s.title} label={s.label} value={s.value} />
                    </div>
                );
            }) : <div className="loader">Loading...</div>}
        </div>
    )
};

export default DonationStats;
