const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

const entries = {
  app: './js/app.js',
  bootstrap: './scss/bootstrap.scss',
  'font-awesome': './scss/font-awesome.scss',
  main: './scss/main.scss',
};

module.exports = {
  entry: entries,
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [{
          loader: MiniCssExtractPlugin.loader
        }, {
          loader: 'css-loader'
        }, {
          loader: 'sass-loader',
          options: {
            // outputStyle: 'compressed'
          }
        }]
      },
      // This test block is for extracting files from font-awesome.
      {
        test: /\.(eot|ttf|woff|woff2)$/,
        use: [{
          loader: 'file-loader',
          options: {
            name: '[path][name].[ext]',
            outputPath: 'fonts/'
          }
        }],
      },
      {
        test: /\.(jpg|png|svg)$/,
        use: [{
          loader: 'file-loader',
          options: {
            name: '[path][name].[ext]',
            outputPath: 'images/'
          }
        }],
      }
    ]
  },
  plugins: [
    new MiniCssExtractPlugin({
        filename: "[name].css"
    })
  ],
  optimization: {
    splitChunks: {
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: "vendor",
          chunks: "all"
        }
      }
    }
  },
  output: {
    filename: '[name].js',
    path: path.resolve(__dirname, '..', 'assets')
  }
};

