import { useState } from 'react';
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
    const stripe = useStripe();
    const elements = useElements();

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
        if (result.error) {
            // Inform the user if there was an error.
            setError(result.error.message);
        } else {
            setError(null);
            // Send the token to your server.
            stripeTokenHandler(result.token);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <div className="form-row">
                <label for="card-element">
                    Credit or debit card
                </label>
                <CardElement
                    id="card-element"
                    options={CARD_ELEMENT_OPTIONS}
                    onChange={handleChange}
                />
                <div className="card-errors" role="alert">{error}</div>
            </div>
            <button type="submit">Submit Payment</button>
        </form>
    );
};

export default ({ stripeKey }) => {
    const stripePromise = loadStripe('pk_test_V5JYKHDsRowNf2IiF9K2L5WE00Wcn7a6oS');

    return (
        <Elements stripe={stripePromise}>
            <CheckoutForm/>
        </Elements>
    );
};
//
