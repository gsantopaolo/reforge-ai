/*
 * JBoss, Home of Professional Open Source
 * Copyright 2015, Red Hat, Inc. and/or its affiliates, and individual
 * contributors by the @authors tag. See the copyright.txt in the
 * distribution for a full listing of individual contributors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.jboss.as.quickstarts.kitchensink.util;

import java.util.ResourceBundle;

/**
 * Helper class to load application resources.
 */
public class Resources {

    private static final ResourceBundle MESSAGE_BUNDLE = ResourceBundle.getBundle("Messages");

    private Resources() {
        // Prevent instantiation
    }

    /**
     * Get a string from the resource bundle.
     *
     * @param key Key for the resource bundle string.
     * @return String value for the given key.
     */
    public static String getString(String key) {
        return MESSAGE_BUNDLE.getString(key);
    }
}
