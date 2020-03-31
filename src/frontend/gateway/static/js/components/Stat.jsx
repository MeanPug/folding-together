import React from 'react';

const Stat = ({ title, label, value }) => {
    return (
         <div className="text-left">
             <strong className="uppercase text-sm block pb-2">{title}</strong>
             <span className="text-lg text-gray-600">{label}</span>

             <h3 className="uppercase text-3xl pt-2 tracking-wide">{value}</h3>
         </div>
    );
};

export default Stat;
