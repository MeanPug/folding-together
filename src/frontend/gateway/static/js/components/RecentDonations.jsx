import React from 'react';

const RecentDonations = ({ n }) => {
    return (
        <ul className="folding-recent-donations">
            <li className="border-b border-dotted border-gray-200 py-2">
                <p><span className="italic text-sm pr-6">20 minutes</span><strong>Bobby</strong> Donated <strong>$4</strong></p>
            </li>
            <li className="border-b border-dotted border-gray-200 py-2">
                <p><span className="italic text-sm pr-6">30 minutes</span><strong>John</strong> Donated <strong>$4</strong></p>
            </li>
        </ul>
    )
};

export default RecentDonations;
