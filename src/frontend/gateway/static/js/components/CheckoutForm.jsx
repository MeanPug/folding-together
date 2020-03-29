import { useState } from 'react';
import React from 'react';
import { chargePaymentMethod } from '../lib/payments';
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
    const [firstName, setFirstName] = useState(null);
    const [lastName, setLastName] = useState(null);
    const [email, setEmail] = useState(null);
    const [donationAmount, setDonationAmount] = useState(1);
    // may be set depending on the stripe flow taken
    let donationId = null;

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

    async function handleStripeJsResult(result) {
        if (result.status === 'error') {
            setError(result.message);
        } else {
            // The card action has been handled
            // The PaymentIntent can be confirmed again on the server
            const serverResponse = await chargePaymentMethod({
                first_name: firstName,
                last_name: lastName,
                email: email,
                donation_amount: donationAmount,
                donation_id: donationId,
                payment_intent_id: result.paymentIntent.id
            });

            handleServerResponse(serverResponse);
        }
    }

    function handleServerResponse(response) {
        if (response.status === 'error') {
            setError(response.message);
        } else if (response.status === 'requires_action') {
            donationId = response.donation_id;
            // Use Stripe.js to handle required card action
            stripe
                .handleCardAction(response.payment_intent_client_secret)
                .then(handleStripeJsResult);
        } else {
            window.location = response.redirect;
        }
    }

    // Handle form submission.
    const handleSubmit = async (event) => {
        event.preventDefault();
        const result = await stripe.createPaymentMethod({
            type: 'card',
            card: elements.getElement(CardElement),
            billing_details: {
                // Include any additional collected billing details.
                name: `${firstName} ${lastName}`,
                email
            },
        });
        const validation = validateData();

        if (result.error) {
            setError(result.error.message);
        } else if (validation.error) {
            setError(validation.error)
        } else {
            setError(null);
            const serverResponse = await chargePaymentMethod({
                first_name: firstName,
                last_name: lastName,
                email: email,
                donation_amount: donationAmount,
                payment_method_id: result.paymentMethod.id
            });

            handleServerResponse(serverResponse);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2 className="pb-4 text-lg uppercase">Donation Information</h2>

            <div className="flex flex-col sm:flex-row">
                <div className="w-full sm:w-1/2 pr-0 sm:pr-4">
                    <input
                        type="text"
                        name="first_name"
                        placeholder="First Name"
                        className="form-field"
                        value={firstName}
                        onChange={evt => setFirstName(evt.currentTarget.value)}
                    />
                </div>

                <div className="w-full sm:w-1/2 pl-0 sm:pl-4 mt-2 sm:mt-0">
                    <input
                        type="text"
                        name="last_name"
                        placeholder="Last Name"
                        className="form-field"
                        value={lastName}
                        onChange={evt => setLastName(evt.currentTarget.value)}
                    />
                </div>
            </div>

            <div className="flex flex-col sm:flex-row items-end pt-4">
                <div className="w-full sm:w-1/2 pr-0 sm:pr-4">
                    <input
                        type="email"
                        name="email"
                        placeholder="Email"
                        title="only required if you want a report of how your donation was spent"
                        className="form-field"
                        value={email}
                        onChange={evt => setEmail(evt.currentTarget.value)}
                    />
                </div>

                <div className="w-full sm:w-1/2 pl-0 sm:pl-4 mt-2 sm:mt-0">
                    <label htmlFor="donation" className="text-gray-700 italic">Donation Amount</label>

                    <div className="flex items-center">
                        <span>$</span>
                        <input
                            type="number"
                            name="donation"
                            className="form-field"
                            placeholder="0"
                            onChange={evt => setDonationAmount(evt.currentTarget.value)}
                            value={donationAmount}
                        />
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
