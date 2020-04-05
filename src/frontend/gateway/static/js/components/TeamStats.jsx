import React from 'react';
import { useState } from 'react';
import { formatNumber } from "../lib/formatting";
import Stat from './Stat.jsx';
import config from "../config";

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
                label: 'Folding@Together team contributions relative to all teams on the network',
                value: `${formatNumber(fahData.rank)} / ${formatNumber(fahData.teams)}`
            },
            {
                title: 'Work Units',
                label: 'the number of units of work contributed by the Folding@Together team',
                value: `${fahData.wus} WUS`
            },
        ];
    }

    const retrieveFahData = async function() {
        const teamDataRoute = `https://cors-anywhere.herokuapp.com/https://api.foldingathome.org/team/${config.TEAM_ID}`;
        const teamCountRoute = `https://cors-anywhere.herokuapp.com/https://api.foldingathome.org/team/count`;

        const teamDataResponse = await fetch(teamDataRoute, {
            method: 'GET',
            headers: {
                'Accepts': 'application/json'
            }
        });
        const teamCountResponse = await fetch(teamCountRoute, {
            method: 'GET'
        });

        const data = await teamDataResponse.json();
        data.teams = await teamCountResponse.text();

        setFahData(data);
    };

    if (!fahData.id) {
        retrieveFahData();
    }

    return (
        <div className="flex flex-col lg:flex-row items-start w-full sm:w-3/4 lg:w-full">
            {fahData.id ? stats.map((s, ix) => {
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

export default TeamStats;
