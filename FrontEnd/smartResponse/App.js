import {createAppContainer} from 'react-navigation';
import {createStackNavigator} from 'react-navigation-stack';
import {Welcome} from './Welcome.js'

const MainNavigator = createStackNavigator({
  Home: {screen: Welcome},
  //Profile: {screen: ProfileScreen},
});

const App = createAppContainer(MainNavigator);

export default App;