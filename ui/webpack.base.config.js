const path = require("path");
const webpack = require('webpack');
const port = process.env.PORT || 3000;

module.exports = {
    mode: 'development',
    entry: {
        // Add as many entry points as you have container-react-components here
        App: './src/App.jsx',
        vendors: ['react']
    },

    output: {
        path: path.resolve('../src/static/bundles/local/'),
        filename: "[name]-[hash].js",
        publicPath: '/'
    },

    devtool: 'inline-source-map',

    externals: [], // add all vendor libs

    module: {
        rules: [
            {
                test: /\.(js)$/,
                exclude: /node_modules/,
                use: ['babel-loader']
            },
            {
                test: /\.(jsx)$/,
                exclude: /node_modules/,
                use: ['babel-loader']
            },
        ]
    },

    optimization: {
        splitChunks: {
            cacheGroups: {
                vendors: {
                    chunks: 'initial',
                    test: 'vendors',
                    name: 'vendors',
                    enforce: true
                }
            }
        }
    },

    plugins: [
        new webpack.HotModuleReplacementPlugin(),
    ], // add all common plugins here

    devServer: {
        host: 'localhost',
        port: port,
        historyApiFallback: true,
        open: true,
        hot: true
    },

    resolve: {
        extensions: [".js", ".jsx", ".json"]
    }
};
