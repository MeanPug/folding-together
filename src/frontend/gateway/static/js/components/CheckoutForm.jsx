import { useState } from 'react';
import React from 'react';
import { chargeToken } from '../lib/payments';
import { loadStripe } from '@stripe/stripe-js';
import {
    CardElement,
    Elements,
    useElements,
    useStripe
} from '@stripe/react-stripe-js';

// Custom styling can be passed to options when creating an Element.
const CARD_ELEMENT_OPTIONS = {
    style: {
        base: {
            color: '#32325d',
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
                color: '#aab7c4'
            }
        },
        invalid: {
            color: '#fa755a',
            iconColor: '#fa755a'
        }
    }
};

const CheckoutForm = () => {
    const [error, setError] = useState(null);
    const [donationAmount, setDonationAmount] = useState(1);
    const stripe = useStripe();
    const elements = useElements();

    const validateData = () => {
        // the donation amount must be >= 1
        if (donationAmount < 1) {
            return {
                error: 'please set a donation amount greater than or equal to $1'
            }
        }

        return {
            error: null
        }
    };

    // Handle real-time validation errors from the card Element.
    const handleChange = (event) => {
        if (event.error) {
            setError(event.error.message);
        } else {
            setError(null);
        }
    };

    // Handle form submission.
    const handleSubmit = async (event) => {
        event.preventDefault();
        const card = elements.getElement(CardElement);
        const result = await stripe.createToken(card);
        const validation = validateData();

        if (result.error) {
            setError(result.error.message);
        } else if (validation.error) {
            setError(validation.error)
        } else {
            setError(null);
            chargeToken(result.token);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2 className="pb-4 text-lg uppercase">Donation Information</h2>

            <div className="flex">
                <div className="w-1/2 pr-4">
                    <input type="text" name="first_name" placeholder="First Name" className="form-field" />
                </div>

                <div className="w-1/2 pl-4">
                    <input type="text" name="last_name" placeholder="Last Name" className="form-field" />
                </div>
            </div>

            <div className="flex items-end pt-4">
                <div className="w-1/2 pr-4">
                    <input type="email" name="email" placeholder="Email" title="only required if you want a report of how your donation was spent" className="form-field" />
                </div>

                <div className="w-1/2 pl-4">
                    <label htmlFor="donation" className="text-gray-700 italic">Donation Amount</label>

                    <div className="flex items-center">
                        <span>$</span>
                        <input type="number" name="donation" className="form-field" placeholder="0" onChange={evt => setDonationAmount(evt.currentTarget.value)} value={donationAmount} />
                    </div>
                </div>
            </div>

            <h2 className="pt-12 pb-4 text-lg uppercase">Payment Information</h2>

            <div className="form-row">
                <CardElement
                    id="card-element"
                    options={CARD_ELEMENT_OPTIONS}
                    onChange={handleChange}
                />
                <div className="card-errors pt-8 text-center font-bold text-sm text-orange" role="alert">{error}</div>
            </div>

            <div className="text-center pt-8">
                <button type="submit" className="btn-primary bg-orange text-white">Send ${donationAmount} Donation</button>
            </div>
        </form>
    );
};

export default ({ stripeKey }) => {
    const stripePromise = loadStripe(stripeKey);

    return (
        <Elements stripe={stripePromise}>
            <CheckoutForm/>
        </Elements>
    );
};
