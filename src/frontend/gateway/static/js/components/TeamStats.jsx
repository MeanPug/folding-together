import React from 'react';
import { useState } from 'react';
import { formatNumber } from "../lib/formatting";
import config from "../config";

const Stat = ({ title, label, value }) => {
    return (
         <div className="text-left">
             <strong className="uppercase text-sm block">{title}</strong>
             <span className="text-lg text-gray-600">{label}</span>

             <h3 className="uppercase text-3xl pt-2 tracking-wide">{value}</h3>
         </div>
    );
};

const TeamStats = ({ donationCount }) => {
    const [fahData, setFahData] = useState({});
    let stats = [];
    if (fahData.id) {
        stats = [
            {
                title: "Donations",
                label: "the number of donors contributing to the Folding@Together team",
                value: donationCount
            },
            {
                title: 'Rank',
                label: 'the number of donors contributing to the Folding@Together team',
                value: `${formatNumber(fahData.rank)} / ${formatNumber(fahData.teams)}`
            },
            {
                title: 'Work Units',
                label: 'the number of donors contributing to the Folding@Together team',
                value: `${fahData.wus} WUS`
            },
        ];
    }

    const retrieveFahData = async function() {
        const apiRoute = `https://cors-anywhere.herokuapp.com/https://api.foldingathome.org/team/${config.TEAM_ID}`;
        const response = await fetch(apiRoute, {
            method: 'GET',
            headers: {
                'Accepts': 'application/json'
            }
        });
        const data = await response.json();
        setFahData(data);
    };

    if (!fahData.id) {
        retrieveFahData();
    }

    return (
        <div className="flex items-center">
            {fahData.id ? stats.map((s, ix) => (
                <div className={ix > 0 ? 'px-4 md:px-8 mx-4' : ''}>
                    <Stat title={s.title} label={s.label} value={s.value} />
                </div>
            )) : <div className="loader">Loading...</div>}
        </div>
    )
};

export default TeamStats;
