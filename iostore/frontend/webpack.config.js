const path = require("path");
const webpack = require("webpack");

module.exports = {
  entry: path.join(__dirname, "src", "index.js"),
  output: {
    path: path.join(__dirname, "static","frontend"),
    filename: "main.js",
  },
  module: {
    rules: [
      { 
        test: /\.(js|jsx)$/, 
        exclude: /node_modules/, 
        use: ["babel-loader"] 
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"],
      },
      { 
        test: /\.(jpg|jpeg|png|gif|mp3|svg)$/,
        use: ["file-loader"] 
      },
    ],
  },
  optimization: {
    minimize: true,
  },
  plugins: [
    new webpack.DefinePlugin({
        'process.env.NODE_ENV': JSON.stringify("development")
    }),
  ],
};