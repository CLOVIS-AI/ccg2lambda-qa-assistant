package utils

import java.util.*

/**
 * Convenience method to get a [ResourceBundle].
 *
 * @param name The name of the bundle
 * @param locale The locale of the bundle (by default, English)
 * @return The bundle in the required locale
 * @throws MissingResourceException if there is no such bundle
 * @see ResourceBundle.getBundle
 */
fun bundle(name: String, locale: Locale = Locale.ENGLISH): ResourceBundle = ResourceBundle.getBundle(name, locale)

/**
 * Convenience operator to get info from a [ResourceBundle].
 *
 * @see ResourceBundle.getString
 */
operator fun ResourceBundle.get(name: String): String = getString(name)

operator fun <T> List<T>.get(range: IntRange) = range.map { this[it] }