const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const webpack = require('webpack');
let path = require('path');

module.exports = {
    plugins: [
        new MiniCssExtractPlugin(),
        new webpack.EnvironmentPlugin({
            STRIPE_PUBLIC_KEY: null,
        })
    ],
    entry: ['babel-polyfill', path.resolve(__dirname, 'gateway/static/js/site.js')],
    output: {
        path: path.resolve(__dirname, 'gateway/static/build'),
        filename: '[name].js'
    },
    module: {
        rules: [
            {
                test: /\.m?jsx?$/,
                exclude: /(node_modules|bower_components)/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env', '@babel/preset-react']
                    }
                }
            },
            {
                test: /\.css$/,
                use: [MiniCssExtractPlugin.loader, 'css-loader', 'postcss-loader']
            }
        ]
    }
};
