import { message } from 'antd';
import { authActions } from './auth.actions';

// Display error to user as a UI notification and log it to console
export const displayError = (error: Error) => {
  try {
    message.error(error.toString(), 5);
  } catch (e) {
    // to make jsdom tests work
    return;
  } finally {
    // tslint:disable-next-line:no-console
    console.error(error);
  }
};

// moveItem moves an item in a given array up (toward index zero) or down (toward the last index),
// returning a new array
export type MoveItem<T> = (array: Array<T>, index: number, direction: 'up' | 'down') => Array<T>;
export const moveItem: MoveItem<any> = (array, index, direction) => {
  let newArray = [...array];
  if (direction === 'up') {
    if (index === 0) return newArray;
    newArray[index - 1] = array[index];
    newArray[index] = array[index - 1];
  } else if (direction === 'down') {
    if (index >= array.length - 1) return newArray;
    newArray[index + 1] = array[index];
    newArray[index] = array[index + 1];
  } else {
    throw new Error('Invalid direction');
  }
  return newArray;
};

// Wrapper around the standard 'fetch' that takes care of:
// - Adding jwt to request header
// - Decoding JSON response and adding the response status code to decoded JSON object
export const jwtFetch = (path: string, options?: object) => {
  const jwt = window.localStorage.getItem('jwt');
  if (jwt === null) {
    const error = 'JWT not found in local storage. You must be logged in.';
    message.error(error);
  }

  const newOptions = {
    ...options,
    headers: {
      'Content-type': 'application/json',
      Authorization: 'JWT ' + jwt
    }
  };

  return fetch(path, newOptions).then(response => {
    // Need to figure this response out. openLogin triggers modal to popup,
    // but in next cycle. Keep track of request, and after submit on modal
    // run jwt fetch again?
    if (response.status === 401) {
      authActions.update({
        openLogin: true,
        loggedIn: false,
      });
      return;
    }
    if (response.status !== 200) {
      displayError(new Error(`HTTP ${response.status} on ${path}`));
    }
    return response.json().then(json => {
      // Always add statusCode to the data object or array returned by response.json()
      let copy: any;
      if ('length' in json) {
        // array
        copy = [...json];
        (copy as any).statusCode = response.status;
      } else {
        // object
        copy = { ...json, statusCode: response.status };
      }
      return copy;
    });
  });
};

export const timeout = (ms: number) => {
      return new Promise(resolve => setTimeout(resolve, ms));
};
