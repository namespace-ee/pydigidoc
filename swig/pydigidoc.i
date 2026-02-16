/* pydigidoc - Python-specific SWIG wrapper for libdigidocpp
 *
 * Thin wrapper that adds snake_case renaming and includes the upstream
 * SWIG interface. No patching needed — upstream libdigidocpp.i already
 * has Python typemaps, director support, and exception handling.
 */

/* Suppress warnings for nested classes (SWIG limitation) */
#pragma SWIG nowarn=325

/* Global camelCase -> snake_case renaming for all functions and methods.
   Must appear BEFORE %include of upstream interface. */
%rename("%(undercase)s", %$isfunction) "";
%rename("%(undercase)s", %$ismember, %$not %$isenumitem, %$not %$isconstant, %$not %$isenum) "";

/* Include upstream libdigidocpp SWIG interface (already has Python typemaps,
   director support, exception handling, template instantiations, %newobject).

   DEPENDENCY: Upstream declares %module(directors="1") digidoc — our SWIG_MODULE_NAME
   in CMakeLists.txt is set to "digidoc" to match. If upstream changes the module name
   or drops directors, this build will break. */
%include "libdigidocpp.i"
