
# Set defaults if not defined already:
%define rpm_device flo
%define rpm_vendor flo

%define __requires_exclude ^.*$
%define __provides_exclude_from ^%{_libexecdir}/droid-hybris/.*$
%define android_root .
%define dhd_path rpm/dhd

# On the OBS this package should be built in the i486 scheduler against
# mer/sailfish *_i486 targets.
# The prjconf should have an ExportFilter like this (mer/sailfish has this):
#   ExportFilter: \.armv7hl\.rpm$ armv8el
# We lie about our architecture and allows OBS to cross-publish this 486 cross-built spec to the armv7hl repos
%if 0%{?device_target_cpu:1}
%define _target_cpu %{device_target_cpu}
%else
%define _target_cpu armv7hl
%endif

# Support build info extracted from OBS builds too
%if 0%{?_obs_build_project:1}
%define _build_flavour %(echo %{_obs_build_project} | awk -F : '{if ($NF == "testing" || $NF == "release") print $NF; else if ($NF ~ /[0-9]\.[0-9]\.[0-9]/ && NF == 3) print strdevel; else if (NF == 2) print strdevel; else print strunknown}' strdevel=devel strunknown=unknown)
%else
%define _build_flavour unknown
%endif

%define _obs_build_count %(echo %{release} | awk -F . '{if (NF >= 3) print $3; else print $1 }')
%define _obs_commit_count %(echo %{release} | awk -F . '{if (NF >= 2) print $2; else print $1 }')

%if "%{_build_flavour}" == "release"
%define _version_appendix (%{_target_cpu})
%else
%define _version_appendix (%{_target_cpu},%{_build_flavour})
%endif

# Don't run strip
%define __strip /bin/true

Summary: 	Droid HAL package for flo
License: 	BSD-3-Clause
Name: 		droid-hal-flo-img-boot
Version: 	0.0.6
# timestamped releases are used only for HADK (mb2) builds
%if 0%{?_obs_build_project:1}
Release: 	1
%else
%define rel_date %(date +'%%Y%%m%%d%%H%%M')
Release: 	%{rel_date}
%endif
Provides: droid-hal-img-boot

################
Group:	System
Requires: oneshot
%{_oneshot_requires_post}
BuildRequires:  droid-hal-deb-img-boot
Summary: Boot img for droid-hal device: flo

%description
The boot.img for device

################################################################
# Begin prep/build section

%prep
# No %%setup macro !!


%build


################
%install
rm -rf $RPM_BUILD_ROOT
# Create dir structure
mkdir -p $RPM_BUILD_ROOT/boot
cp -a /boot/hybris-boot.img /boot/hybris-updater-unpack.sh /boot/hybris-updater-script /boot/update-binary $RPM_BUILD_ROOT/boot
sed -i -e 's/deb/flo/g' $RPM_BUILD_ROOT/boot/hybris-updater-script

################################################################
# Begin pre/post section


################################################################
# Begin files section

%files
%defattr(644,root,root,-)
/boot/hybris-boot.img
/boot/update-binary
/boot/hybris-updater-script
/boot/hybris-updater-unpack.sh
