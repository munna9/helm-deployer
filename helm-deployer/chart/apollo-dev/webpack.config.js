const nodeExternals = require("webpack-node-externals");
const path = require("path");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");

module.exports = {
  module: {
    rules: [
      {
        exclude: [path.resolve(__dirname, "node_modules")],
        test: /\.ts$/,
        use: "ts-loader"
      }
    ]
  },
  output: {
    filename: "main.js",
    path: path.resolve(__dirname, "dist")
  },
  resolve: {
    extensions: [".ts", ".js"]
  },
  target: "node",
  devtool: "source-map",
  entry: [path.join(__dirname, "src/main.ts")],
  externals: [nodeExternals({})],
  mode: "development",
  plugins: [new CleanWebpackPlugin()]
};
