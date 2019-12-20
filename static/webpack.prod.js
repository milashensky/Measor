const webpack = require('webpack')
const merge = require('webpack-merge')
const common = require('./webpack.config.js')
const TerserPlugin = require('terser-webpack-plugin');
const path = require('path')

module.exports = merge(common, {
    mode: 'production',
    output: {
        publicPath: '/static/assets/',
        path: path.resolve(__dirname, './assets'),
        filename: `app.js?[hash]`
    },
    devtool: '#source-map',
    optimization: {
        minimize: true,
        minimizer: [new TerserPlugin()],
    }
});
module.exports.plugins = (common.plugins || []).concat([
    new webpack.DefinePlugin({
        'process.env': {
            'NODE_ENV': JSON.stringify('production')
        }
    }),
    new webpack.optimize.OccurrenceOrderPlugin()
]);
