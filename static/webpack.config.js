var path = require('path')
var webpack = require('webpack')

module.exports = {
     mode: 'development',
     entry: './src/index.js',
     output: {
          publicPath: '/static/assets/',
          path: path.resolve(__dirname, './assets'),
          filename: 'app.js'
     },
     module: {
          rules: [
               {
                    test: /\.(js|jsx)$/,
                    exclude: /node_modules/,
                    use: {
                         loader: "babel-loader"
                    }
               },
               {
                    test: /\.css$/,
                    use: ['style-loader', 'css-loader']
               },
               {
                    test: /\.(png|jpg|gif|ttf|svg|woff|woff2|eot|ico)$/,
                    exclude: [/\.inline\.svg$/],
                    loader: 'file-loader',
                    options: {
                         name: '[name].[ext]?[hash]'
                    }
               },
               {
                    test: /\.inline\.svg$/,
                    use: [
                         {
                              loader: "babel-loader"
                         }, {
                              loader: "react-svg-loader",
                              options: {
                                   jsx: true // true outputs JSX tags
                              }
                         }
                    ]
               }
          ]
     },
     resolve: {
          alias: {
               '@': path.resolve('./src'),
               'styles': path.resolve('./src/styles'),
               'pages': path.resolve('./src/pages')
          },
          extensions: ['*', '.js', '.jsx', '.json']
     },
     devtool: '#eval-source-map',
     plugins: [
          // new webpack.DefinePlugin({
          //     'window.apiUrl': '"http://localhost:8006/api/"'
          // }),
          new webpack.HotModuleReplacementPlugin(),
          new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/)
     ]
}
