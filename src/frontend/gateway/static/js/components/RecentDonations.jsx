import React from 'react';

const RecentDonations = ({ donations }) => {
    return (
        <ul className="folding-recent-donations">
            {donations.map(donation => (
                <li className="border-b border-dotted border-gray-200 py-2 flex justify-between">
                    <span className="italic text-sm pr-6">{donation.time_canonical}</span>
                    <div>
                        <a href={donation.url}>
                            <strong className="block">{donation.name}</strong>
                            Donated <strong>{donation.amount}</strong>
                        </a>
                    </div>
                </li>
            ))}
        </ul>
    )
};

export default RecentDonations;
